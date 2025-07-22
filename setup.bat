@echo off
REM Modrinth Modpack Updater - Windows Setup Script

echo 🚀 Setting up Modrinth Modpack Updater...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH.
    echo    Please install Python 3.8+ from: https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% detected

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available. Please reinstall Python with pip included.
    pause
    exit /b 1
)

REM Ask about virtual environment
set /p CREATE_VENV="🔧 Create a virtual environment? (recommended) [y/N]: "
if /i "%CREATE_VENV%"=="y" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    
    REM Activate virtual environment
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment created and activated
    echo    To activate it later, run: venv\Scripts\activate.bat
)

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Test installation
echo 🧪 Testing installation...
python update_modpack.py --help >nul 2>&1

if %errorlevel% neq 0 (
    echo ❌ Installation test failed
    pause
    exit /b 1
)

echo ✅ Installation test passed

REM Success message
echo.
echo 🎉 Setup complete! You can now use the Modrinth Modpack Updater.
echo.
echo 📖 Quick start examples:
echo    python update_modpack.py --modpack-dir .\examples\fabric-example --client
echo    python update_modpack.py --modpack-dir path\to\modpack --client --server
echo.
echo 📚 For more information, see README.md or run:
echo    python update_modpack.py --help
echo.
echo 🌟 Don't forget to star the repository if you find it useful!
echo.
pause
