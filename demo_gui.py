#!/usr/bin/env python3
"""
GUI Demo Script

Demonstrates the LunarBit Modpack Updater GUI with sample data.
This script shows what the interface looks like without requiring a real modpack.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import ModpackUpdaterGUI, LunarBitTheme
except ImportError:
    print("Error: Could not import GUI module. Please ensure gui.py is in the same directory.")
    sys.exit(1)

class DemoGUI(ModpackUpdaterGUI):
    """Demo version of the GUI with sample data pre-filled"""
    
    def setup_variables(self):
        """Initialize with demo data"""
        super().setup_variables()
        # Pre-fill with example data
        self.modpack_path.set("examples/simple-modpack/")
        self.generate_client.set(True)
        self.generate_server.set(False)
        self.overrides_folder.set("overrides")
        
    def start_update(self):
        """Demo version that shows sample output instead of running real update"""
        if not self.modpack_path.get():
            messagebox.showerror("Error", "Please select a modpack folder or .mrpack file")
            return
            
        # Update UI state
        self.is_running = True
        self.update_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress.start()
        
        # Clear output and show demo content
        self.output_text.delete(1.0, tk.END)
        self.show_demo_output()
        
    def show_demo_output(self):
        """Show sample output to demonstrate the interface"""
        demo_lines = [
            "🚀 Starting modpack update...\n",
            f"📁 Modpack: {self.modpack_path.get()}\n", 
            "⚙️ Command: python3 update_modpack.py --modpack-dir examples/simple-modpack/ --client\n",
            "-" * 50 + "\n\n",
            "🔍 Scanning modpack directory...\n",
            "📄 Found modrinth.index.json\n",
            "📦 Detected modpack: Simple Modpack v1.0.0\n",
            "🎯 Target: Minecraft 1.21.4, Fabric\n\n",
            "🔄 Checking for mod updates...\n",
            "✅ Sodium: mc1.21.4-0.6.0 → mc1.21.4-0.6.13 (update available)\n",
            "✅ Fabric API: 0.104.0+1.21 → 0.129.0+1.21.4 (update available)\n", 
            "✅ JEI: 19.22.4.118 (up to date)\n",
            "✅ REI: 16.0.744 (up to date)\n\n",
            "📥 Downloading updated mods...\n",
            "⬇️  Downloading Sodium mc1.21.4-0.6.13...\n",
            "⬇️  Downloading Fabric API 0.129.0+1.21.4...\n\n",
            "📂 Exporting to local mods/ directory...\n",
            "💾 Exported 4 mods to mods/\n\n",
            "📦 Generating client .mrpack...\n",
            "🔧 Creating modpack structure...\n",
            "📄 Writing modrinth.index.json...\n",
            "📁 Adding overrides folder...\n",
            "🗜️  Compressing to Simple-Modpack.mrpack...\n\n",
            "📊 Update Summary:\n",
            "   🔄 Updated: 2 mods\n",
            "   ✅ Up-to-date: 2 mods\n",
            "   ❌ Failed: 0 mods\n\n",
            "✅ Update completed successfully!\n",
            "🎉 Generated: Simple-Modpack.mrpack\n"
        ]
        
        # Add lines with delay to simulate real-time output
        self.demo_line_index = 0
        self.demo_lines = demo_lines
        self.add_demo_line()
        
    def add_demo_line(self):
        """Add one line of demo output with timing"""
        if self.demo_line_index < len(self.demo_lines) and self.is_running:
            line = self.demo_lines[self.demo_line_index]
            self.output_text.insert(tk.END, line)
            self.output_text.see(tk.END)
            self.demo_line_index += 1
            
            # Schedule next line (vary timing for realism)
            delay = 200 if line.startswith("⬇️") else 100
            if line.startswith("🔄") or line.startswith("📥"):
                delay = 500
            
            self.root.after(delay, self.add_demo_line)
        else:
            # Demo finished
            self.is_running = False
            self.update_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.progress.stop()

def main():
    """Launch the demo GUI"""
    root = tk.Tk()
    
    # Show info about demo mode
    messagebox.showinfo(
        "Demo Mode", 
        "🎭 This is a DEMO of the LunarBit Modpack Updater GUI.\n\n"
        "• Sample data is pre-filled\n"
        "• Update button shows simulated output\n"
        "• No actual modpack updates are performed\n\n"
        "To use the real version, run: python3 run_gui.py"
    )
    
    app = DemoGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
