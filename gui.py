#!/usr/bin/env python3
"""
Modrinth Modpack Updater - GUI Version

A beautiful GUI interface for the Modrinth Modpack Updater with LunarBit theming.
Provides an intuitive way to update modpacks and generate .mrpack files.

Author: LunarBit
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import sys
import subprocess
from pathlib import Path

# Add the current directory to path to import the main script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class LunarBitTheme:
    """LunarBit color scheme and styling"""
    
    # Dark theme colors inspired by modern dev tools
    BACKGROUND = "#0d1117"          # Deep dark background
    SURFACE = "#161b22"             # Card/surface background
    SURFACE_VARIANT = "#21262d"     # Elevated surfaces
    PRIMARY = "#58a6ff"             # Bright blue accent
    PRIMARY_VARIANT = "#1f6feb"     # Darker blue
    SECONDARY = "#f85149"           # Red accent
    SUCCESS = "#3fb950"             # Green for success
    WARNING = "#d29922"             # Yellow for warnings
    TEXT_PRIMARY = "#f0f6fc"        # Primary text color
    TEXT_SECONDARY = "#8b949e"      # Secondary text color
    TEXT_MUTED = "#6e7681"          # Muted text
    BORDER = "#30363d"              # Border color
    HOVER = "#30363d"               # Hover state
    
    @classmethod
    def configure_style(cls):
        """Configure ttk styles with LunarBit theme"""
        style = ttk.Style()
        
        # Configure main theme
        style.theme_use('clam')
        
        # Configure colors
        style.configure('.',
                       background=cls.BACKGROUND,
                       foreground=cls.TEXT_PRIMARY,
                       fieldbackground=cls.SURFACE,
                       bordercolor=cls.BORDER,
                       focuscolor=cls.PRIMARY,
                       selectbackground=cls.PRIMARY,
                       selectforeground=cls.TEXT_PRIMARY)
        
        # Button styles
        style.configure('Accent.TButton',
                       background=cls.PRIMARY,
                       foreground=cls.TEXT_PRIMARY,
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Accent.TButton',
                 background=[('active', cls.PRIMARY_VARIANT),
                           ('pressed', cls.PRIMARY_VARIANT)])
        
        style.configure('Secondary.TButton',
                       background=cls.SURFACE_VARIANT,
                       foreground=cls.TEXT_PRIMARY,
                       borderwidth=1,
                       bordercolor=cls.BORDER,
                       focuscolor='none',
                       padding=(15, 8))
        
        style.map('Secondary.TButton',
                 background=[('active', cls.HOVER),
                           ('pressed', cls.HOVER)])
        
        # Frame styles
        style.configure('Card.TFrame',
                       background=cls.SURFACE,
                       borderwidth=1,
                       relief='solid',
                       bordercolor=cls.BORDER)
        
        # Label styles
        style.configure('Heading.TLabel',
                       background=cls.SURFACE,
                       foreground=cls.TEXT_PRIMARY,
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Subheading.TLabel',
                       background=cls.SURFACE,
                       foreground=cls.TEXT_SECONDARY,
                       font=('Segoe UI', 10))
        
        # Entry styles
        style.configure('TEntry',
                       fieldbackground=cls.SURFACE_VARIANT,
                       bordercolor=cls.BORDER,
                       insertcolor=cls.TEXT_PRIMARY,
                       borderwidth=1)
        
        # Checkbutton styles
        style.configure('TCheckbutton',
                       background=cls.SURFACE,
                       foreground=cls.TEXT_PRIMARY,
                       focuscolor='none',
                       borderwidth=0)
        
        # Progressbar styles
        style.configure('TProgressbar',
                       background=cls.PRIMARY,
                       troughcolor=cls.SURFACE_VARIANT,
                       borderwidth=0,
                       lightcolor=cls.PRIMARY,
                       darkcolor=cls.PRIMARY)

class ModpackUpdaterGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_queue()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("LunarBit Modpack Updater")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set window icon if available
        try:
            icon_path = Path(__file__).parent / "icon.png"
            if icon_path.exists():
                self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
        except:
            pass
        
        # Configure theme
        LunarBitTheme.configure_style()
        self.root.configure(bg=LunarBitTheme.BACKGROUND)
        
    def setup_variables(self):
        """Initialize tkinter variables"""
        self.modpack_path = tk.StringVar()
        self.generate_client = tk.BooleanVar()
        self.generate_server = tk.BooleanVar()
        self.overrides_folder = tk.StringVar(value="overrides")
        self.is_running = False
        
    def setup_queue(self):
        """Setup queue for thread communication"""
        self.output_queue = queue.Queue()
        self.root.after(100, self.check_queue)
        
    def setup_ui(self):
        """Create the user interface"""
        # Main container with padding
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Left panel - Configuration
        left_panel = self.create_config_panel(content_frame)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Right panel - Output
        right_panel = self.create_output_panel(content_frame)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Logo and title area
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill='x', padx=20, pady=15)
        
        # Title
        title_label = ttk.Label(title_frame, 
                               text="🚀 LunarBit Modpack Updater",
                               style='Heading.TLabel',
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(anchor='w')
        
        # Subtitle
        subtitle_label = ttk.Label(title_frame,
                                  text="Intelligent Modrinth modpack updating with client/server generation",
                                  style='Subheading.TLabel')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
    def create_config_panel(self, parent):
        """Create the configuration panel"""
        config_frame = ttk.Frame(parent, style='Card.TFrame')
        config_frame.configure(width=350)
        config_frame.pack_propagate(False)
        
        # Panel header
        header_frame = ttk.Frame(config_frame)
        header_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        ttk.Label(header_frame, text="⚙️ Configuration", 
                 style='Heading.TLabel').pack(anchor='w')
        
        # Configuration content
        content_frame = ttk.Frame(config_frame)
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Modpack selection
        self.create_modpack_selection(content_frame)
        
        # Options
        self.create_options_section(content_frame)
        
        # Action buttons
        self.create_action_buttons(content_frame)
        
        return config_frame
        
    def create_modpack_selection(self, parent):
        """Create modpack file/folder selection"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(section_frame, text="Modpack Location",
                 style='Heading.TLabel',
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        ttk.Label(section_frame, text="Select a modpack folder or .mrpack file",
                 style='Subheading.TLabel').pack(anchor='w', pady=(2, 8))
        
        # Path selection frame
        path_frame = ttk.Frame(section_frame)
        path_frame.pack(fill='x', pady=(0, 10))
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.modpack_path,
                                   font=('Consolas', 10))
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="Browse",
                               command=self.browse_modpack,
                               style='Secondary.TButton')
        browse_btn.pack(side='right')
        
    def create_options_section(self, parent):
        """Create options section"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(section_frame, text="Generation Options",
                 style='Heading.TLabel',
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        ttk.Label(section_frame, text="Choose what to generate after updating",
                 style='Subheading.TLabel').pack(anchor='w', pady=(2, 12))
        
        # Checkboxes
        client_cb = ttk.Checkbutton(section_frame, 
                                   text="📱 Generate client .mrpack",
                                   variable=self.generate_client)
        client_cb.pack(anchor='w', pady=2)
        
        server_cb = ttk.Checkbutton(section_frame,
                                   text="🖥️ Generate server .mrpack",
                                   variable=self.generate_server)
        server_cb.pack(anchor='w', pady=2)
        
        # Overrides folder
        ttk.Label(section_frame, text="Overrides Folder",
                 style='Heading.TLabel',
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(15, 0))
        
        ttk.Label(section_frame, text="Folder containing configs and resources",
                 style='Subheading.TLabel').pack(anchor='w', pady=(2, 8))
        
        overrides_entry = ttk.Entry(section_frame, textvariable=self.overrides_folder,
                                   font=('Consolas', 10))
        overrides_entry.pack(fill='x')
        
    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(20, 0))
        
        self.update_btn = ttk.Button(button_frame,
                                    text="🚀 Update Modpack",
                                    command=self.start_update,
                                    style='Accent.TButton')
        self.update_btn.pack(fill='x', pady=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame,
                                  text="⏹️ Stop",
                                  command=self.stop_update,
                                  style='Secondary.TButton',
                                  state='disabled')
        self.stop_btn.pack(fill='x')
        
    def create_output_panel(self, parent):
        """Create the output panel"""
        output_frame = ttk.Frame(parent, style='Card.TFrame')
        
        # Panel header
        header_frame = ttk.Frame(output_frame)
        header_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        ttk.Label(header_frame, text="📋 Output Log", 
                 style='Heading.TLabel').pack(side='left')
        
        # Clear button
        clear_btn = ttk.Button(header_frame, text="Clear",
                              command=self.clear_output,
                              style='Secondary.TButton')
        clear_btn.pack(side='right')
        
        # Output text area
        output_container = ttk.Frame(output_frame)
        output_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.output_text = scrolledtext.ScrolledText(
            output_container,
            wrap=tk.WORD,
            bg=LunarBitTheme.SURFACE_VARIANT,
            fg=LunarBitTheme.TEXT_PRIMARY,
            insertbackground=LunarBitTheme.TEXT_PRIMARY,
            selectbackground=LunarBitTheme.PRIMARY,
            selectforeground=LunarBitTheme.TEXT_PRIMARY,
            font=('Consolas', 10),
            borderwidth=1,
            relief='solid'
        )
        self.output_text.pack(fill='both', expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(output_container, mode='indeterminate')
        self.progress.pack(fill='x', pady=(10, 0))
        
        return output_frame
        
    def browse_modpack(self):
        """Open file/folder browser for modpack selection"""
        current_path = self.modpack_path.get()
        initial_dir = os.path.dirname(current_path) if current_path else os.getcwd()
        
        # Try to select folder first
        folder = filedialog.askdirectory(
            title="Select Modpack Folder",
            initialdir=initial_dir
        )
        
        if folder:
            self.modpack_path.set(folder)
            return
            
        # If no folder selected, try file
        file = filedialog.askopenfilename(
            title="Select .mrpack File",
            initialdir=initial_dir,
            filetypes=[("Modrinth Modpack", "*.mrpack"), ("All Files", "*.*")]
        )
        
        if file:
            self.modpack_path.set(file)
            
    def start_update(self):
        """Start the modpack update process"""
        if not self.modpack_path.get():
            messagebox.showerror("Error", "Please select a modpack folder or .mrpack file")
            return
            
        if not os.path.exists(self.modpack_path.get()):
            messagebox.showerror("Error", "Selected modpack path does not exist")
            return
            
        # Update UI state
        self.is_running = True
        self.update_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress.start()
        
        # Clear output
        self.output_text.delete(1.0, tk.END)
        
        # Start update in separate thread
        self.update_thread = threading.Thread(target=self.run_update, daemon=True)
        self.update_thread.start()
        
    def run_update(self):
        """Run the modpack update in a separate thread"""
        try:
            # Build command
            script_path = Path(__file__).parent / "update_modpack.py"
            cmd = [sys.executable, str(script_path), "--modpack-dir", self.modpack_path.get()]
            
            if self.generate_client.get():
                cmd.append("--client")
            if self.generate_server.get():
                cmd.append("--server")
            if self.overrides_folder.get():
                cmd.extend(["--overrides-folder", self.overrides_folder.get()])
                
            self.output_queue.put(f"🚀 Starting modpack update...\n")
            self.output_queue.put(f"📁 Modpack: {self.modpack_path.get()}\n")
            self.output_queue.put(f"⚙️ Command: {' '.join(cmd)}\n")
            self.output_queue.put("-" * 50 + "\n\n")
            
            # Run the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            if process.stdout:
                for line in process.stdout:
                    if not self.is_running:
                        process.terminate()
                        break
                    self.output_queue.put(line)
                
            # Wait for process to complete
            process.wait()
            
            if process.returncode == 0:
                self.output_queue.put(f"\n✅ Update completed successfully!\n")
            else:
                self.output_queue.put(f"\n❌ Update failed with exit code {process.returncode}\n")
                
        except Exception as e:
            self.output_queue.put(f"\n❌ Error: {str(e)}\n")
        finally:
            self.output_queue.put("DONE")
            
    def stop_update(self):
        """Stop the running update"""
        self.is_running = False
        self.output_queue.put("\n⏹️ Update stopped by user\n")
        
    def check_queue(self):
        """Check for messages from the update thread"""
        try:
            while True:
                message = self.output_queue.get_nowait()
                if message == "DONE":
                    # Update finished
                    self.is_running = False
                    self.update_btn.config(state='normal')
                    self.stop_btn.config(state='disabled')
                    self.progress.stop()
                    break
                else:
                    # Add message to output
                    self.output_text.insert(tk.END, message)
                    self.output_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queue)
        
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)

def main():
    """Main entry point for the GUI"""
    root = tk.Tk()
    app = ModpackUpdaterGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
