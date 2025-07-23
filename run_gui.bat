@echo off
REM LunarBit Modpack Updater - GUI Launcher for Windows

echo Starting LunarBit Modpack Updater GUI...
python run_gui.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo Error starting GUI. Please ensure Python is installed and in your PATH.
    pause
)
