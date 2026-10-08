@echo off

echo ==========================================
echo Accessibility Automation - Setup
echo ==========================================

echo.
echo Creating virtual environment...

python -m venv .venv

if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not available in PATH.
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...

call .venv\Scripts\activate.bat

echo.
echo Upgrading pip...

python -m pip install --upgrade pip

echo.
echo Installing Python dependencies...

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install Python dependencies.
    pause
    exit /b 1
)

echo.
echo Installing Playwright browsers...

playwright install

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install Playwright browsers.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================

echo.
echo You can now run:
echo.
echo     run.bat
echo.

pause