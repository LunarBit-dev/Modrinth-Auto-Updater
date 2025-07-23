#!/usr/bin/env python3
"""
LunarBit Modpack Updater - Unified Launcher

Universal launcher that can run the modpack updater in either CLI or GUI mode.
Automatically detects the best mode based on arguments and environment.

Usage:
    python3 launcher.py                           # Launch GUI (default)
    python3 launcher.py --gui                     # Launch GUI explicitly  
    python3 launcher.py --cli [CLI_OPTIONS]       # Launch CLI mode
    python3 launcher.py --modpack-dir PATH        # Launch CLI mode (auto-detected)
"""

import sys
import os
import argparse
from pathlib import Path

def has_gui_support():
    """Check if GUI is supported in the current environment"""
    try:
        import tkinter
        # Test if we can create a Tk instance (may fail in headless environments)
        root = tkinter.Tk()
        root.withdraw()  # Hide the test window
        root.destroy()
        return True
    except (ImportError, Exception):
        return False

def show_mode_selection():
    """Show a simple console-based mode selection"""
    print("🚀 LunarBit Modpack Updater")
    print("=" * 40)
    print()
    print("Choose how to run the updater:")
    print("1. 🎨 GUI Mode (Recommended)")
    print("2. 💻 CLI Mode")
    print("3. ❌ Cancel")
    print()
    
    while True:
        try:
            choice = input("Enter choice (1-3): ").strip()
            if choice == "1":
                return "gui"
            elif choice == "2":
                return "cli"
            elif choice == "3":
                return "cancel"
            else:
                print("Please enter 1, 2, or 3")
        except (KeyboardInterrupt, EOFError):
            return "cancel"

def launch_gui():
    """Launch the GUI version"""
    try:
        from gui import main as gui_main
        print("🎨 Launching GUI mode...")
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI module: {e}")
        print("Please ensure gui.py is available in the same directory.")
        return False
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        return False
    return True

def launch_cli(args):
    """Launch the CLI version with given arguments"""
    try:
        # Import and run the CLI script
        import update_modpack
        
        # Prepare sys.argv for the CLI script
        original_argv = sys.argv.copy()
        sys.argv = ['update_modpack.py'] + args
        
        print("💻 Launching CLI mode...")
        print(f"🔧 Arguments: {' '.join(args)}")
        print("-" * 50)
        
        try:
            update_modpack.main()
        finally:
            # Restore original argv
            sys.argv = original_argv
            
    except ImportError as e:
        print(f"❌ Error importing CLI module: {e}")
        print("Please ensure update_modpack.py is available in the same directory.")
        return False
    except Exception as e:
        print(f"❌ Error running CLI: {e}")
        return False
    return True

def main():
    """Main launcher function"""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="LunarBit Modpack Updater - Universal Launcher",
        add_help=False  # We'll handle help ourselves
    )
    
    # Add our launcher-specific arguments
    parser.add_argument('--gui', action='store_true', 
                       help='Launch GUI mode explicitly')
    parser.add_argument('--cli', action='store_true',
                       help='Launch CLI mode explicitly')
    parser.add_argument('--help', '-h', action='store_true',
                       help='Show this help message')
    
    # Parse known args to separate launcher args from CLI args
    launcher_args, cli_args = parser.parse_known_args()
    
    # Show help
    if launcher_args.help:
        print("🚀 LunarBit Modpack Updater - Universal Launcher")
        print("=" * 55)
        print()
        parser.print_help()
        print()
        print("CLI Mode Options:")
        print("  When using --cli, you can pass any options supported by update_modpack.py")
        print("  Example: python3 launcher.py --cli --modpack-dir ./MyModpack --client")
        print()
        print("Auto-Detection:")
        print("  If you provide CLI arguments without --cli, CLI mode will be auto-selected")
        print("  Example: python3 launcher.py --modpack-dir ./MyModpack")
        return
    
    # Determine mode
    mode = None
    
    if launcher_args.gui:
        mode = "gui"
    elif launcher_args.cli or cli_args:
        mode = "cli"
    else:
        # No explicit mode specified, try to determine automatically
        if has_gui_support():
            # GUI is available, let user choose or default to GUI
            if sys.stdin.isatty():  # Interactive terminal
                mode = show_mode_selection()
                if mode == "cancel":
                    print("👋 Goodbye!")
                    return
            else:
                # Non-interactive, default to GUI
                mode = "gui"
        else:
            # No GUI support, force CLI
            mode = "cli"
            print("ℹ️ GUI not available, using CLI mode")
    
    # Launch the selected mode
    if mode == "gui":
        if not has_gui_support():
            print("❌ GUI mode is not available in this environment")
            print("💻 Falling back to CLI mode...")
            mode = "cli"
        else:
            success = launch_gui()
            if not success:
                print("💻 Falling back to CLI mode...")
                mode = "cli"
    
    if mode == "cli":
        if not cli_args:
            # No CLI args provided, show CLI help
            print("💻 CLI mode selected but no arguments provided.")
            print("📖 Showing CLI help:")
            print()
            try:
                import update_modpack
                original_argv = sys.argv.copy()
                sys.argv = ['update_modpack.py', '--help']
                try:
                    update_modpack.main()
                except SystemExit:
                    pass  # Normal exit from argparse help
                finally:
                    sys.argv = original_argv
            except ImportError:
                print("❌ CLI module not available")
        else:
            success = launch_cli(cli_args)
            if not success:
                sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
