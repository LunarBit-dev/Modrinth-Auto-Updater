#!/bin/bash
# LunarBit Modpack Updater - GUI Launcher for Mac/Linux

echo "Starting LunarBit Modpack Updater GUI..."

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    python3 run_gui.py
elif command -v python &> /dev/null; then
    python run_gui.py
else
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.8 or later"
    exit 1
fi
