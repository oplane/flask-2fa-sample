# 🔐 Flask 2FA Authentication App

A Flask web application demonstrating user authentication with Two-Factor Authentication (2FA) using Time-based One-Time Password (TOTP).

> **⚠️ EDUCATIONAL/DEMONSTRATION PURPOSE ONLY**  
> This application is designed to demonstrate basic 2FA implementation. It lacks several critical security features required for production use.

## Features

- ✅ **User Registration & Login** - Secure account creation and authentication
- ✅ **Password Hashing** - Passwords are hashed using bcrypt with salt
- ✅ **Two-Factor Authentication (2FA)** - Optional TOTP-based 2FA
- ✅ **QR Code Generation** - Easy 2FA setup with QR codes
- ✅ **Session Management** - User session handling with Flask-Login
- ✅ **Protected Routes** - Dashboard accessible only to authenticated users
- ✅ **Modern UI** - Clean, responsive design with beautiful styling
- ✅ **Basic Input Validation** - Password length requirements and user input validation

## Technology Stack

- **Backend**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **2FA**: PyOTP (TOTP implementation)
- **Password Hashing**: bcrypt
- **QR Code**: qrcode library with Pillow
- **Frontend**: HTML5, CSS3 (modern responsive design)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone or navigate to the project directory**
```bash
cd /Users/emil/workspace/flask-2fa
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
```

3. **Activate the virtual environment**
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set environment variables (optional)**

Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here-change-this-in-production
DATABASE_URL=sqlite:///app.db
```

Or export them directly:
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite:///app.db"
```

6. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage Guide

### 1. Register a New Account

1. Navigate to `http://localhost:5000`
2. Click on "Register here"
3. Choose a username (3-80 characters)
4. Create a strong password (minimum 8 characters)
5. Confirm your password
6. Click "Register"

### 2. Login Without 2FA

1. Go to the login page
2. Enter your username and password
3. Click "Login"
4. You'll be redirected to the dashboard

### 3. Enable Two-Factor Authentication

1. From the dashboard, click "Enable 2FA"
2. Install an authenticator app on your phone:
   - Google Authenticator
   - Microsoft Authenticator
   - Authy
   - 1Password
3. Scan the QR code with your authenticator app
4. Enter the 6-digit code shown in the app
5. Click "Enable 2FA"
6. 2FA is now active for your account!

### 4. Login With 2FA

1. Go to the login page
2. Enter your username and password
3. You'll be redirected to the 2FA verification page
4. Open your authenticator app
5. Enter the 6-digit code
6. You'll be logged in to your dashboard

### 5. Disable 2FA

1. From the dashboard, click "Disable 2FA"
2. Confirm the action
3. 2FA is now disabled for your account

## Project Structure

```
flask-2fa/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── verify_2fa.html # 2FA verification page
│   ├── setup_2fa.html  # 2FA setup page
│   └── dashboard.html  # Protected dashboard
└── static/             # Static files
    └── css/
        └── style.css   # Application styles
```

## Security Features

### ✅ Implemented Security Features

#### Password Security
- Passwords are hashed using bcrypt with unique salt per user
- Minimum password length requirement (8 characters)
- Password confirmation during registration
- No plaintext passwords stored

#### Two-Factor Authentication
- TOTP (Time-based One-Time Password) implementation
- 30-second time window for codes
- QR code for easy setup with authenticator apps
- Optional 2FA (users can choose to enable/disable it)

#### Session Management
- User session management with Flask-Login
- Protected routes requiring authentication
- Session-based 2FA verification flow

#### Database Security
- SQL injection prevention with SQLAlchemy ORM
- Parameterized queries

#### Access Control
- `@login_required` decorator on protected routes
- User can only manage their own 2FA settings

## API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/` | GET | Home page (redirects) | No |
| `/register` | GET, POST | User registration | No |
| `/login` | GET, POST | User login | No |
| `/verify-2fa` | GET, POST | 2FA verification | No (session) |
| `/dashboard` | GET | Protected dashboard | Yes |
| `/setup-2fa` | GET, POST | Enable 2FA | Yes |
| `/qrcode` | GET | Generate QR code | Yes |
| `/disable-2fa` | POST | Disable 2FA | Yes |
| `/logout` | GET | User logout | Yes |

## Database Schema

### User Table
- `id` (Integer, Primary Key)
- `username` (String, Unique, Required)
- `password_hash` (String, Required)
- `totp_secret` (String, Optional) - **⚠️ Stored in plaintext**
- `is_2fa_enabled` (Boolean, Default: False)
- `created_at` (DateTime)

## Development

### Running in Development Mode

The application runs in debug mode by default when executed with `python app.py`. Debug mode provides:
- Automatic reloading on code changes
- Detailed error messages
- Interactive debugger

### Database Initialization

The database is automatically created when you first run the application. To reset the database:

```bash
rm app.db
python app.py
```

## Production Deployment

**⚠️ WARNING: This application is NOT production-ready in its current state.**

This is a demonstration/educational project. Before deploying to production, you MUST:

### Critical Security Requirements

1. **Implement Rate Limiting** - Add Flask-Limiter or similar to prevent brute-force attacks
2. **Add Account Lockout** - Lock accounts after failed login attempts
3. **Encrypt TOTP Secrets** - Use Fernet or similar to encrypt 2FA secrets in database
4. **Configure Secure Cookies** - Add HttpOnly, Secure, SameSite flags
5. **Add CSRF Protection** - Implement Flask-WTF or similar
6. **Implement Audit Logging** - Log all authentication events
7. **Add Input Validation** - Enhanced validation for all user inputs

### Deployment Steps (After Security Fixes)

1. **Set a strong SECRET_KEY**
```bash
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
```

2. **Use a production WSGI server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Use a production database**
Replace SQLite with PostgreSQL or MySQL:
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

4. **Enable HTTPS**
Use a reverse proxy like Nginx with SSL/TLS certificates (Required for secure cookies)

5. **Set up monitoring and alerting**
Monitor failed login attempts and security events

## Testing

To test the application:

1. Register a new user
2. Login without 2FA
3. Enable 2FA from the dashboard
4. Logout and login again (should prompt for 2FA)
5. Verify 2FA with authenticator app
6. Access the protected dashboard
7. Test disable 2FA functionality

## Troubleshooting

### Issue: Database errors
**Solution**: Delete `app.db` and restart the application to recreate the database

### Issue: 2FA codes not working
**Solution**: Ensure your system time is synchronized (TOTP requires accurate time)

### Issue: QR code not displaying
**Solution**: Check that all dependencies are installed, especially `qrcode` and `Pillow`

### Issue: Import errors
**Solution**: Ensure you've activated the virtual environment and installed all requirements

## Purpose & Scope

This is an **educational demonstration project** created to showcase:
- Basic Flask web application structure
- User authentication implementation
- Two-factor authentication (TOTP) integration
- QR code generation for authenticator apps
- Session management with Flask-Login

**Not intended for:**
- Production deployment without significant security enhancements
- Handling sensitive or real user data
- Enterprise or commercial applications

## Contributing

This demonstration project is provided as-is for educational purposes. Feel free to:
- Fork and modify for learning
- Use as a starting point for more secure implementations
- Submit issues or improvements

## License

This project is open source and available for educational and personal use.

## Credits

Created as a basic 2FA authentication demonstration using Flask. Generated via Cursor AI based on the prompt: *"You are an expert developer. Develop a secure flask app accompanied by a .html page. The feature is that the user can login with two factor and then view an authenticated page."*

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyOTP Documentation](https://pyotp.readthedocs.io/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [TOTP RFC 6238](https://tools.ietf.org/html/rfc6238)

## Support

For issues, questions, or contributions, please refer to the project repository.

---

**Happy Coding! 🚀**

