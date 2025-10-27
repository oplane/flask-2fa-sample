import os
import io
import bcrypt
import pyotp
import qrcode
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Rate limiting constants
LOCKOUT_THRESHOLD = 5
LOCKOUT_TIME = timedelta(minutes=15)
FAILED_LOGIN_RESET_TIME = timedelta(hours=1)  # Reset failed login counter after 1 hour

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    totp_secret = db.Column(db.String(32), nullable=True)
    is_2fa_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Rate limiting and brute-force protection fields
    failed_logins = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime, nullable=True)
    account_locked_until = db.Column(db.DateTime, nullable=True)
    failed_2fa_attempts = db.Column(db.Integer, default=0)
    last_failed_2fa = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify the user's password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def generate_totp_secret(self):
        """Generate a new TOTP secret for 2FA"""
        self.totp_secret = pyotp.random_base32()
        return self.totp_secret
    
    def get_totp_uri(self):
        """Get the provisioning URI for QR code generation"""
        return pyotp.totp.TOTP(self.totp_secret).provisioning_uri(
            name=self.username,
            issuer_name='Flask 2FA App'
        )
    
    def verify_totp(self, token):
        """Verify a TOTP token"""
        if not self.totp_secret:
            return False
        totp = pyotp.TOTP(self.totp_secret)
        return totp.verify(token, valid_window=1)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def is_account_locked(user):
    """Check if a user account is currently locked"""
    if user.account_locked_until and user.account_locked_until > datetime.utcnow():
        return True
    return False

def should_reset_failed_attempts(user, attempt_type='login'):
    """Check if failed attempts should be reset based on time elapsed"""
    if attempt_type == 'login':
        if user.last_failed_login and (datetime.utcnow() - user.last_failed_login) > FAILED_LOGIN_RESET_TIME:
            return True
    elif attempt_type == '2fa':
        if user.last_failed_2fa and (datetime.utcnow() - user.last_failed_2fa) > FAILED_LOGIN_RESET_TIME:
            return True
    return False

def get_rate_limit_key():
    """Get rate limit key based on username from form or IP address"""
    username = request.form.get('username', '').strip()
    if username:
        return f"user:{username}"
    return f"ip:{get_remote_address()}"

# Routes
@app.route('/')
def index():
    """Home page - redirects to dashboard if logged in"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per hour", key_func=get_rate_limit_key)
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute; 20 per hour", key_func=get_rate_limit_key)
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(username=username).first()
        
        # Reset failed attempts if enough time has passed
        if user and should_reset_failed_attempts(user, 'login'):
            user.failed_logins = 0
            user.last_failed_login = None
            db.session.commit()
        
        # Check if account is locked (even if user doesn't exist, timing attack prevention)
        if user and is_account_locked(user):
            minutes_remaining = int((user.account_locked_until - datetime.utcnow()).total_seconds() / 60)
            flash(f'Account locked due to too many failed attempts. Try again in {minutes_remaining} minutes.', 'error')
            return render_template('login.html')
        
        # Verify credentials
        if user and user.check_password(password):
            # Reset failed login attempts on successful authentication
            user.failed_logins = 0
            user.account_locked_until = None
            user.last_failed_login = None
            db.session.commit()
            
            # If 2FA is enabled, redirect to 2FA verification
            if user.is_2fa_enabled:
                session['pending_user_id'] = user.id
                return redirect(url_for('verify_2fa'))
            else:
                # Login without 2FA
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        else:
            # Track failed login attempt
            if user:
                user.failed_logins += 1
                user.last_failed_login = datetime.utcnow()
                
                # Lock account if threshold reached
                if user.failed_logins >= LOCKOUT_THRESHOLD:
                    user.account_locked_until = datetime.utcnow() + LOCKOUT_TIME
                    db.session.commit()
                    flash('Account locked due to too many failed attempts. Please try again later.', 'error')
                    return render_template('login.html')
                
                db.session.commit()
            
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/verify-2fa', methods=['GET', 'POST'])
@limiter.limit("5 per minute; 20 per hour", key_func=lambda: f"2fa:{session.get('pending_user_id', get_remote_address())}")
def verify_2fa():
    """2FA verification page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    pending_user_id = session.get('pending_user_id')
    if not pending_user_id:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(pending_user_id)
    if not user:
        session.pop('pending_user_id', None)
        flash('User not found', 'error')
        return redirect(url_for('login'))
    
    # Reset failed 2FA attempts if enough time has passed
    if should_reset_failed_attempts(user, '2fa'):
        user.failed_2fa_attempts = 0
        user.last_failed_2fa = None
        db.session.commit()
    
    # Check if account is locked
    if is_account_locked(user):
        session.pop('pending_user_id', None)
        minutes_remaining = int((user.account_locked_until - datetime.utcnow()).total_seconds() / 60)
        flash(f'Account locked due to too many failed attempts. Try again in {minutes_remaining} minutes.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        
        if user.verify_totp(token):
            # Reset failed 2FA attempts on success
            user.failed_2fa_attempts = 0
            user.last_failed_2fa = None
            session.pop('pending_user_id', None)
            db.session.commit()
            
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Track failed 2FA attempt
            user.failed_2fa_attempts += 1
            user.last_failed_2fa = datetime.utcnow()
            
            # Lock account if threshold reached
            if user.failed_2fa_attempts >= LOCKOUT_THRESHOLD:
                user.account_locked_until = datetime.utcnow() + LOCKOUT_TIME
                session.pop('pending_user_id', None)
                db.session.commit()
                flash('Account locked due to too many failed 2FA attempts. Please try again later.', 'error')
                return redirect(url_for('login'))
            
            db.session.commit()
            flash('Invalid 2FA code. Please try again.', 'error')
    
    return render_template('verify_2fa.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Protected dashboard page"""
    return render_template('dashboard.html', user=current_user)

@app.route('/setup-2fa', methods=['GET', 'POST'])
@login_required
def setup_2fa():
    """Setup 2FA for the current user"""
    if current_user.is_2fa_enabled:
        flash('2FA is already enabled for your account', 'info')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        
        if current_user.verify_totp(token):
            current_user.is_2fa_enabled = True
            db.session.commit()
            flash('2FA has been successfully enabled!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid 2FA code. Please try again.', 'error')
    else:
        # Generate new TOTP secret if not already present
        if not current_user.totp_secret:
            current_user.generate_totp_secret()
            db.session.commit()
    
    return render_template('setup_2fa.html')

@app.route('/qrcode')
@login_required
def get_qrcode():
    """Generate and return QR code for 2FA setup"""
    if not current_user.totp_secret:
        return "No TOTP secret found", 404
    
    # Generate QR code
    uri = current_user.get_totp_uri()
    img = qrcode.make(uri)
    
    # Convert to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

@app.route('/disable-2fa', methods=['POST'])
@login_required
def disable_2fa():
    """Disable 2FA for the current user"""
    current_user.is_2fa_enabled = False
    current_user.totp_secret = None
    db.session.commit()
    flash('2FA has been disabled', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    """Logout the current user"""
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Database initialization
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
