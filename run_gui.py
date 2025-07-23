#!/usr/bin/env python3
"""
LunarBit Modpack Updater - GUI Launcher

Quick launcher for the GUI version of the modpack updater.
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the GUI"""
    # Add current directory to path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    try:
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI module: {e}")
        print("Please ensure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
