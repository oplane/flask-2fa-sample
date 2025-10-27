# 🚀 Quick Start Guide

Get your Flask 2FA app running in 3 easy steps!

## Option 1: Using the Start Script (Recommended)

### macOS/Linux
```bash
./run.sh
```

### Windows
```cmd
run.bat
```

## Option 2: Manual Setup

### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 2: Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the App
```bash
python app.py
```

## Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## First Time Usage

1. **Register**: Create a new account with username and password
2. **Login**: Sign in with your credentials
3. **Dashboard**: View your protected dashboard
4. **Enable 2FA** (Optional):
   - Click "Enable 2FA" on dashboard
   - Scan QR code with authenticator app
   - Enter verification code
   - Done! 2FA is now active

## Recommended Authenticator Apps

- **Google Authenticator** (iOS/Android)
- **Microsoft Authenticator** (iOS/Android)
- **Authy** (iOS/Android)
- **1Password** (iOS/Android/Desktop)

## Common Commands

### Stop the Server
Press `Ctrl + C` in the terminal

### Reset Database
```bash
rm app.db
python app.py
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Troubleshooting

### Port Already in Use
If port 5000 is busy, edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### Module Not Found Error
Make sure virtual environment is activated:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Database Locked Error
Close any other instances of the app and delete `app.db`:
```bash
rm app.db
```

## Need More Help?

See the full [README.md](README.md) for detailed documentation.

---

**Happy coding! 🎉**

