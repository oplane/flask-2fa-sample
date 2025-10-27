@echo off
REM Flask 2FA App Quick Start Script for Windows

echo ================================
echo Flask 2FA Authentication App Setup
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed

REM Set default secret key if not set
if "%SECRET_KEY%"=="" (
    set SECRET_KEY=dev-secret-key-12345
    echo.
    echo Using development SECRET_KEY
)

REM Run the application
echo.
echo Starting Flask application...
echo.
echo ====================================
echo Access the app at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python app.py

