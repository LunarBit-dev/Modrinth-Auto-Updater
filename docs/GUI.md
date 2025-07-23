# GUI Documentation

## Overview

The LunarBit Modpack Updater GUI provides a beautiful, user-friendly interface for updating Minecraft modpacks. Built with tkinter and styled with a modern dark theme inspired by the LunarBit website.

## Features

### 🎨 Modern Design
- **Dark Theme**: Easy on the eyes with LunarBit's signature dark colors
- **Responsive Layout**: Adjusts to different window sizes
- **Professional Styling**: Modern card-based layout with proper spacing

### 🚀 Easy to Use
- **Browse Button**: Easily select modpack folders or .mrpack files
- **Configuration Panel**: All options in one convenient location
- **Real-time Output**: Live progress monitoring with colored terminal output
- **Progress Indicator**: Visual feedback during long-running operations

### ⚙️ Full Feature Set
All command-line features are available in the GUI:
- Modpack updating with intelligent version checking
- Client .mrpack generation
- Server .mrpack generation with compatibility filtering
- Custom overrides folder configuration

## Color Scheme

The GUI uses LunarBit's signature color palette:

- **Background**: `#0d1117` - Deep dark background
- **Surface**: `#161b22` - Card backgrounds
- **Primary**: `#58a6ff` - Blue accent color
- **Success**: `#3fb950` - Green for success states
- **Warning**: `#d29922` - Yellow for warnings
- **Error**: `#f85149` - Red for errors
- **Text**: `#f0f6fc` - Primary text color

## Layout

### Left Panel - Configuration
- **Modpack Selection**: Browse for folders or .mrpack files
- **Generation Options**: Toggle client/server .mrpack creation
- **Overrides Configuration**: Specify custom overrides folder
- **Action Buttons**: Start/stop update operations

### Right Panel - Output
- **Live Log**: Real-time output from the update process
- **Progress Bar**: Visual indication of operation status
- **Clear Button**: Reset the output area

## Usage

1. **Launch**: Run `python3 run_gui.py` or use the platform-specific launchers
2. **Select Modpack**: Click "Browse" to choose your modpack folder or .mrpack file
3. **Configure Options**: Enable client/server generation as needed
4. **Update**: Click "🚀 Update Modpack" to start the process
5. **Monitor**: Watch the real-time output for progress and results

## Keyboard Shortcuts

- **Ctrl+Q**: Quit application (on supported platforms)
- **Escape**: Stop running update (when focused on stop button)

## Requirements

- Python 3.8 or higher
- tkinter (included with most Python installations)
- All dependencies from `requirements.txt`

## Troubleshooting

### GUI Won't Start
- Ensure Python 3.8+ is installed
- Check that tkinter is available: `python3 -c "import tkinter"`
- Try running directly: `python3 gui.py`

### No Output During Update
- The GUI runs the CLI script in the background
- Output should appear in real-time in the right panel
- Check that `update_modpack.py` exists in the same directory

### Styling Issues
- The GUI automatically configures its theme
- If colors look wrong, check your system's display settings
- Try restarting the application
