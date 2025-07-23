# Enhanced GUI Documentation

## Overview

The LunarBit Modpack Updater GUI provides a stunning, user-friendly interface for updating Minecraft modpacks. Built with tkinter and styled with an enhanced dark theme inspired by the LunarBit website, featuring modern design elements and improved usability.

## New Features

### 🎨 Enhanced Modern Design
- **Refined Dark Theme**: Updated LunarBit color palette with subtle gradients and enhanced contrast
- **Responsive Layout**: Better proportions and spacing that adapt to different window sizes
- **Professional Typography**: Improved font choices including Cascadia Code for terminal output
- **Card-based Layout**: Enhanced visual hierarchy with better borders and shadows

### 🚀 Improved User Experience
- **Smart File Selection**: Choose between folder or .mrpack file with a beautiful choice dialog
- **Real-time Path Validation**: Instant feedback on selected paths with colored status indicators
- **Enhanced Configuration Panel**: Better organized options with descriptions and visual grouping
- **Live Status Updates**: Dynamic status messages that update based on current operation
- **Improved Progress Tracking**: Enhanced progress indicators with contextual status messages

### ⚙️ Advanced Features
- **Universal Launcher Integration**: Seamlessly launch GUI or CLI mode from a single entry point
- **Enhanced Error Handling**: Better validation and user-friendly error messages
- **Improved Output Display**: Better formatted terminal output with enhanced readability
- **Smart Button Management**: Context-aware button states and improved workflow

## Enhanced Color Scheme

The GUI uses an enhanced LunarBit color palette with improved contrast and modern styling:

- **Background**: `#0d1117` - Deep dark background
- **Surface**: `#161b22` - Card backgrounds  
- **Surface Variant**: `#21262d` - Elevated surfaces
- **Surface Hover**: `#30363d` - Interactive hover states
- **Primary**: `#58a6ff` - Blue accent color
- **Primary Light**: `#79c0ff` - Lighter blue for highlights
- **Success**: `#3fb950` - Green for success states
- **Warning**: `#d29922` - Yellow for warnings
- **Error**: `#f85149` - Red for errors
- **Text Primary**: `#f0f6fc` - Primary text color
- **Text Secondary**: `#8b949e` - Secondary text color
- **Border**: `#30363d` - Enhanced border color

## Enhanced Layout

### Left Panel - Advanced Configuration
- **Enhanced Modpack Selection**: Smart file/folder chooser with visual selection dialog
- **Intelligent Path Validation**: Real-time status indicators with colored feedback
- **Improved Generation Options**: Better organized checkboxes with helpful descriptions
- **Professional Action Buttons**: Enhanced styling with better visual hierarchy

### Right Panel - Live Output Monitor
- **Enhanced Terminal Output**: Better font (Cascadia Code) with improved readability
- **Dynamic Status Updates**: Context-aware status messages that update during operations
- **Professional Progress Tracking**: Enhanced progress bar with detailed status information
- **Smart Output Management**: Better formatted logs with improved visual scanning

## Universal Launcher Integration

### Automatic Mode Detection
```bash
# Launch with auto-detection (GUI preferred)
python3 launcher.py

# Explicit GUI mode
python3 launcher.py --gui

# CLI mode with arguments
python3 launcher.py --cli --modpack-dir ./MyModpack
```

### Smart Fallbacks
- GUI mode automatically falls back to CLI if GUI is unavailable
- Interactive mode selection in terminal environments
- Seamless integration between GUI and CLI functionality

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
