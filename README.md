# 🔐 Flask 2FA Authentication App

A Flask web application demonstrating user authentication with Two-Factor Authentication (2FA) using Time-based One-Time Password (TOTP).

> **⚠️ EDUCATIONAL/DEMONSTRATION PURPOSE ONLY**  
> This application is designed to demonstrate basic 2FA implementation. It lacks several critical security features required for production use. See the [Security Requirements & Implementation Status](#security-requirements--implementation-status) section for a complete analysis of implemented and missing security controls.

## Features

- ✅ **User Registration & Login** - Secure account creation and authentication
- ✅ **Password Hashing** - Passwords are hashed using bcrypt with salt
- ✅ **Two-Factor Authentication (2FA)** - Optional TOTP-based 2FA
- ✅ **QR Code Generation** - Easy 2FA setup with QR codes
- ✅ **Session Management** - User session handling with Flask-Login
- ✅ **Protected Routes** - Dashboard accessible only to authenticated users
- ✅ **Rate Limiting** - Protection against brute-force attacks on login and 2FA
- ✅ **Account Lockout** - Automatic temporary lockout after failed attempts
- ✅ **Modern UI** - Clean, responsive design with beautiful styling
- ✅ **Basic Input Validation** - Password length requirements and user input validation

## Technology Stack

- **Backend**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Rate Limiting**: Flask-Limiter
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

---

## Security Status Overview

**Implementation Score: 3.5/7 Security Requirements**
- ✅ **3 Fully Implemented** (Password Hashing, Access Control, Rate Limiting)
- ⚠️ **1 Partially Implemented** (Input Validation)
- ❌ **3 Not Implemented** (Session Cookies, TOTP Encryption, Audit Logging)

**Critical Security Gaps:**
- 🔴 **Session Cookie Security** (REQ-00000064) - Vulnerable to session hijacking
- 🔴 **TOTP Secret Encryption** (REQ-00000065) - 2FA secrets stored in plaintext

**⚠️ This application should NOT be used in production without implementing all critical security requirements.**

---

## Security Requirements & Implementation Status

This section documents all security requirements identified through threat modeling and their current implementation status.

### Security Requirements Summary

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| REQ-00000063 | Password Hashing and Storage | Critical | ✅ Implemented |
| REQ-00000064 | Session Cookie Security | Critical | ❌ Not Implemented |
| REQ-00000065 | TOTP Secret Encryption | Critical | ❌ Not Implemented |
| REQ-00000066 | Input Validation and Output Encoding | High | ⚠️ Partial |
| REQ-00000067 | Access Control for 2FA Management | High | ✅ Implemented |
| REQ-00000068 | Rate Limiting and Brute-Force Protection | High | ✅ Implemented |
| REQ-00000069 | Audit Logging for Authentication Events | Medium | ❌ Not Implemented |

### Detailed Security Requirements

#### ✅ REQ-00000063: Password Hashing and Storage for User Credentials
**Status**: IMPLEMENTED  
**Priority**: Critical  
**Description**: All user passwords must be hashed using bcrypt with a unique salt per user before storage in the SQLite database. Plaintext passwords must never be stored or logged at any point in the application lifecycle.

**Rationale**: Bcrypt with salt provides strong resistance against brute-force and rainbow table attacks, ensuring user credentials remain protected even if the database is breached.

**Implementation**: See `User.set_password()` and `User.check_password()` methods in `app.py` (lines 52-56).

---

#### ❌ REQ-00000064: Session Cookie Security for Authenticated Users
**Status**: NOT IMPLEMENTED  
**Priority**: Critical  
**Description**: Session cookies used for Flask-Login authentication must be configured with the 'Secure', 'HttpOnly', and 'SameSite=Strict' attributes. Session cookies must be regenerated upon login and logout, and sensitive session data (such as pending user IDs) must be cleared after use.

**Rationale**: Proper session cookie configuration is essential to prevent unauthorized access and ensure that session data cannot be intercepted or manipulated by malicious actors.

**Risk**: Without secure cookie attributes, session hijacking, cross-site scripting (XSS), and cross-site request forgery (CSRF) attacks become possible, allowing attackers to impersonate users or bypass authentication.

**Required Implementation**:
```python
app.config['SESSION_COOKIE_SECURE'] = True      # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True    # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict' # CSRF protection
```

---

#### ❌ REQ-00000065: TOTP Secret Encryption for 2FA Data Storage
**Status**: NOT IMPLEMENTED  
**Priority**: Critical  
**Description**: TOTP secrets generated for users must be encrypted before being stored in the SQLite database. Encryption keys must be securely managed and rotated periodically. TOTP secrets must be deleted from the database when 2FA is disabled.

**Rationale**: Encrypting TOTP secrets protects the integrity of the 2FA system and ensures that even if the database is accessed by unauthorized parties, the secrets remain confidential.

**Risk**: If TOTP secrets are stored in plaintext, a database compromise could allow attackers to generate valid 2FA codes and bypass two-factor authentication.

**Current State**: TOTP secrets are stored in plaintext in the `totp_secret` field (line 41 in `app.py`).

**Required Implementation**: Use Fernet (from `cryptography` library) or similar to encrypt/decrypt secrets with a securely stored master key.

---

#### ⚠️ REQ-00000066: Input Validation and Output Encoding
**Status**: PARTIALLY IMPLEMENTED  
**Priority**: High  
**Description**: All user inputs for registration, login, and 2FA verification must be validated for expected format, length, and type. Output data rendered in templates must be properly encoded to prevent XSS attacks.

**Rationale**: Robust input validation and output encoding are foundational to web application security, preventing common attack vectors that target user-supplied data.

**Current Implementation**:
- ✅ Password length validation (minimum 8 characters)
- ✅ Username and password required checks
- ✅ Password confirmation matching
- ✅ Jinja2 auto-escaping (XSS protection in templates)
- ✅ Basic input sanitization with `.strip()`

**Missing**:
- ❌ Username format validation (special characters, max length enforcement)
- ❌ TOTP token format validation
- ❌ CSRF tokens on forms
- ❌ Comprehensive input sanitization

---

#### ✅ REQ-00000067: Access Control for 2FA Management Endpoints
**Status**: IMPLEMENTED  
**Priority**: High  
**Description**: Endpoints for enabling, disabling, and verifying 2FA (/setup-2fa, /disable-2fa, /verify-2fa) must require authentication and ensure that actions are performed only by the account owner. Authorization checks must be enforced server-side.

**Rationale**: Ensuring that only authenticated and authorized users can manage their own 2FA settings protects account integrity and prevents privilege escalation.

**Implementation**: 
- `@login_required` decorator on `/setup-2fa`, `/disable-2fa`, `/qrcode`
- Uses `current_user` object ensuring user can only manage own 2FA
- See lines 273-274, 299-300, 317-318 in `app.py`

---

#### ✅ REQ-00000068: Rate Limiting and Brute-Force Protection
**Status**: IMPLEMENTED  
**Priority**: High  
**Description**: Implement rate limiting on login and 2FA verification endpoints to restrict the number of attempts per user and IP address. Lock accounts or introduce delays after repeated failed attempts.

**Rationale**: Rate limiting and brute-force protection are critical for defending against automated attacks and ensuring the reliability of authentication mechanisms.

**Implementation**:
- Flask-Limiter integrated with per-IP and per-username rate limits
- Login: 5 attempts/minute, 20/hour
- 2FA verification: 5 attempts/minute, 20/hour
- Registration: 10 attempts/hour
- Account lockout: 5 failed attempts = 15-minute lockout
- Failed attempts tracked in database with timestamps
- Automatic counter reset on successful authentication
- Time-based counter reset: failed attempts reset after 1 hour of inactivity
- See lines 24-35, 84-99, 158-217, 219-273 in `app.py`

---

#### ❌ REQ-00000069: Audit Logging for Authentication and 2FA Events
**Status**: NOT IMPLEMENTED  
**Priority**: Medium  
**Description**: Log all authentication events, including successful and failed login attempts, 2FA setup, verification, and disable actions, with timestamps and user identifiers. Logs must be protected from unauthorized access and tampering.

**Rationale**: Comprehensive audit logs enable monitoring, incident response, and compliance with security best practices.

**Risk**: Lack of audit logging impedes detection of suspicious activity and forensic analysis after a security incident, increasing the risk of undetected breaches.

**Required Implementation**:
- Log all login attempts (success/failure) with timestamps, IP addresses, and usernames
- Log 2FA setup, enable, disable, and verification events
- Log account registration
- Log account lockout events
- Store logs securely (separate from application database)
- Implement log rotation and retention policies

---

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

#### Rate Limiting & Brute-Force Protection
- Login attempts limited to 5 per minute, 20 per hour
- 2FA verification limited to 5 per minute, 20 per hour
- Registration limited to 10 per hour
- Account lockout after 5 failed attempts (15-minute duration)
- Rate limiting by both IP address and username
- Failed attempt tracking in database with timestamps
- Automatic counter reset on successful authentication
- Time-based counter reset: failed attempts automatically reset after 1 hour of inactivity

### ⚠️ Security Limitations

**Critical security features still needed for production:**

- ❌ **Session Cookie Security** (REQ-00000064) - Missing HttpOnly, Secure, SameSite flags
- ❌ **TOTP Secret Encryption** (REQ-00000065) - 2FA secrets stored in plaintext
- ❌ **Audit Logging** (REQ-00000069) - No tracking of security events
- ⚠️ **Input Validation** (REQ-00000066) - Only partially implemented

**See the [Security Requirements & Implementation Status](#security-requirements--implementation-status) section for detailed information about each requirement, including descriptions, rationale, risks, and implementation guidance.**

**⚠️ For production use, implement all critical and high-priority security requirements, and deploy with a production WSGI server behind HTTPS.**

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
- `failed_logins` (Integer, Default: 0)
- `last_failed_login` (DateTime, Optional)
- `account_locked_until` (DateTime, Optional)
- `failed_2fa_attempts` (Integer, Default: 0)
- `last_failed_2fa` (DateTime, Optional)

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

1. **Encrypt TOTP Secrets** - Use Fernet or similar to encrypt 2FA secrets in database
2. **Configure Secure Cookies** - Add HttpOnly, Secure, SameSite flags
3. **Add CSRF Protection** - Implement Flask-WTF or similar
4. **Implement Audit Logging** - Log all authentication events
5. **Add Enhanced Input Validation** - Enhanced validation for all user inputs

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

