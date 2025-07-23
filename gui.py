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
    
    # Enhanced dark theme colors inspired by modern dev tools
    BACKGROUND = "#0d1117"          # Deep dark background
    SURFACE = "#161b22"             # Card/surface background
    SURFACE_VARIANT = "#21262d"     # Elevated surfaces
    SURFACE_HOVER = "#30363d"       # Hover state for surfaces
    PRIMARY = "#58a6ff"             # Bright blue accent
    PRIMARY_VARIANT = "#1f6feb"     # Darker blue
    PRIMARY_LIGHT = "#79c0ff"       # Lighter blue for highlights
    SECONDARY = "#f85149"           # Red accent
    SUCCESS = "#3fb950"             # Green for success
    WARNING = "#d29922"             # Yellow for warnings
    TEXT_PRIMARY = "#f0f6fc"        # Primary text color
    TEXT_SECONDARY = "#8b949e"      # Secondary text color
    TEXT_MUTED = "#6e7681"          # Muted text
    BORDER = "#30363d"              # Border color
    BORDER_SUBTLE = "#21262d"       # Subtle borders
    HOVER = "#30363d"               # Hover state
    
    @classmethod
    def configure_style(cls):
        """Configure ttk styles with enhanced LunarBit theme"""
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
        
        # Enhanced button styles with gradients
        style.configure('Accent.TButton',
                       background=cls.PRIMARY,
                       foreground=cls.TEXT_PRIMARY,
                       borderwidth=0,
                       focuscolor='none',
                       padding=(25, 12),
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Accent.TButton',
                 background=[('active', cls.PRIMARY_VARIANT),
                           ('pressed', cls.PRIMARY_VARIANT),
                           ('focus', cls.PRIMARY_LIGHT)])
        
        style.configure('Secondary.TButton',
                       background=cls.SURFACE_VARIANT,
                       foreground=cls.TEXT_PRIMARY,
                       borderwidth=1,
                       bordercolor=cls.BORDER,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('Segoe UI', 9))
        
        style.map('Secondary.TButton',
                 background=[('active', cls.SURFACE_HOVER),
                           ('pressed', cls.SURFACE_HOVER)],
                 bordercolor=[('active', cls.PRIMARY),
                            ('focus', cls.PRIMARY)])
        
        # Enhanced frame styles
        style.configure('Card.TFrame',
                       background=cls.SURFACE,
                       borderwidth=1,
                       relief='solid',
                       bordercolor=cls.BORDER_SUBTLE)
        
        style.configure('HeaderCard.TFrame',
                       background=cls.SURFACE,
                       borderwidth=2,
                       relief='solid',
                       bordercolor=cls.PRIMARY)
        
        # Enhanced label styles
        style.configure('Heading.TLabel',
                       background=cls.SURFACE,
                       foreground=cls.TEXT_PRIMARY,
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Title.TLabel',
                       background=cls.SURFACE,
                       foreground=cls.TEXT_PRIMARY,
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Subheading.TLabel',
                       background=cls.SURFACE,
                       foreground=cls.TEXT_SECONDARY,
                       font=('Segoe UI', 10))
        
        style.configure('Subtitle.TLabel',
                       background=cls.SURFACE,
                       foreground=cls.TEXT_SECONDARY,
                       font=('Segoe UI', 11))
        
        # Enhanced entry styles
        style.configure('TEntry',
                       fieldbackground=cls.SURFACE_VARIANT,
                       bordercolor=cls.BORDER,
                       insertcolor=cls.TEXT_PRIMARY,
                       borderwidth=2,
                       relief='solid',
                       padding=8)
        
        style.map('TEntry',
                 bordercolor=[('focus', cls.PRIMARY),
                            ('active', cls.PRIMARY)])
        
        # Enhanced checkbutton styles
        style.configure('TCheckbutton',
                       background=cls.SURFACE,
                       foreground=cls.TEXT_PRIMARY,
                       focuscolor='none',
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        # Enhanced progressbar styles
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
        """Configure the main window with enhanced styling"""
        self.root.title("🚀 LunarBit Modpack Updater")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        
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
        
        # Make window resizable with better proportions
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
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
        """Create the enhanced header section"""
        header_frame = ttk.Frame(parent, style='HeaderCard.TFrame')
        header_frame.pack(fill='x', pady=(0, 25))
        
        # Logo and title area with gradient-like styling
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill='x', padx=25, pady=20)
        
        # Title with enhanced styling
        title_label = ttk.Label(title_frame, 
                               text="🚀 LunarBit Modpack Updater",
                               style='Title.TLabel')
        title_label.pack(anchor='w')
        
        # Subtitle with better spacing
        subtitle_label = ttk.Label(title_frame,
                                  text="Intelligent Modrinth modpack updating with client/server generation",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w', pady=(8, 0))
        
        # Version/status info
        status_frame = ttk.Frame(title_frame)
        status_frame.pack(anchor='w', pady=(10, 0))
        
        version_label = ttk.Label(status_frame,
                                 text="v2.0 • Powered by Modrinth API v2",
                                 style='Subheading.TLabel',
                                 font=('Segoe UI', 9))
        version_label.pack(side='left')
        
    def create_config_panel(self, parent):
        """Create the enhanced configuration panel"""
        config_frame = ttk.Frame(parent, style='Card.TFrame')
        config_frame.configure(width=380)
        config_frame.pack_propagate(False)
        
        # Panel header with enhanced styling
        header_frame = ttk.Frame(config_frame)
        header_frame.pack(fill='x', padx=25, pady=(20, 15))
        
        ttk.Label(header_frame, text="⚙️ Configuration", 
                 style='Heading.TLabel',
                 font=('Segoe UI', 13, 'bold')).pack(anchor='w')
        
        # Configuration content with better spacing
        content_frame = ttk.Frame(config_frame)
        content_frame.pack(fill='both', expand=True, padx=25, pady=(0, 25))
        
        # Modpack selection with enhanced styling
        self.create_modpack_selection(content_frame)
        
        # Separator
        separator1 = ttk.Frame(content_frame, height=1, style='Card.TFrame')
        separator1.pack(fill='x', pady=20)
        
        # Options with better organization
        self.create_options_section(content_frame)
        
        # Separator
        separator2 = ttk.Frame(content_frame, height=1, style='Card.TFrame')
        separator2.pack(fill='x', pady=20)
        
        # Action buttons with enhanced styling
        self.create_action_buttons(content_frame)
        
        return config_frame
        
    def create_modpack_selection(self, parent):
        """Create enhanced modpack file/folder selection"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill='x', pady=(0, 0))
        
        ttk.Label(section_frame, text="📁 Modpack Location",
                 style='Heading.TLabel',
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        ttk.Label(section_frame, text="Select a modpack folder or .mrpack file to update",
                 style='Subheading.TLabel').pack(anchor='w', pady=(3, 12))
        
        # Path selection frame with enhanced styling
        path_frame = ttk.Frame(section_frame)
        path_frame.pack(fill='x', pady=(0, 15))
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.modpack_path,
                                   font=('Consolas', 10),
                                   style='TEntry')
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 12))
        
        browse_btn = ttk.Button(path_frame, text="📂 Browse",
                               command=self.browse_modpack,
                               style='Secondary.TButton',
                               width=12)
        browse_btn.pack(side='right')
        
        # Path status indicator
        self.path_status = ttk.Label(section_frame, text="",
                                    style='Subheading.TLabel',
                                    font=('Segoe UI', 9))
        self.path_status.pack(anchor='w')
        
        # Bind to path changes to show status
        self.modpack_path.trace('w', self.update_path_status)
        
    def update_path_status(self, *args):
        """Update the path status indicator"""
        path = self.modpack_path.get()
        if not path:
            self.path_status.config(text="", foreground=LunarBitTheme.TEXT_MUTED)
        elif os.path.exists(path):
            if os.path.isdir(path):
                self.path_status.config(text="✅ Folder selected", 
                                      foreground=LunarBitTheme.SUCCESS)
            elif path.endswith('.mrpack'):
                self.path_status.config(text="✅ .mrpack file selected", 
                                      foreground=LunarBitTheme.SUCCESS)
            else:
                self.path_status.config(text="⚠️ Unknown file type", 
                                      foreground=LunarBitTheme.WARNING)
        else:
            self.path_status.config(text="❌ Path does not exist", 
                                  foreground=LunarBitTheme.SECONDARY)
        
    def create_options_section(self, parent):
        """Create enhanced options section"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill='x', pady=(0, 0))
        
        ttk.Label(section_frame, text="🎯 Generation Options",
                 style='Heading.TLabel',
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        ttk.Label(section_frame, text="Choose what to generate after updating mods",
                 style='Subheading.TLabel').pack(anchor='w', pady=(3, 15))
        
        # Checkboxes with enhanced styling and descriptions
        options_container = ttk.Frame(section_frame)
        options_container.pack(fill='x')
        
        # Client option
        client_frame = ttk.Frame(options_container)
        client_frame.pack(fill='x', pady=3)
        
        client_cb = ttk.Checkbutton(client_frame, 
                                   text="📱 Generate client .mrpack",
                                   variable=self.generate_client,
                                   style='TCheckbutton')
        client_cb.pack(anchor='w')
        
        client_desc = ttk.Label(client_frame,
                               text="   Include client-side mods and configs",
                               style='Subheading.TLabel',
                               font=('Segoe UI', 9))
        client_desc.pack(anchor='w', padx=(20, 0))
        
        # Server option
        server_frame = ttk.Frame(options_container)
        server_frame.pack(fill='x', pady=3)
        
        server_cb = ttk.Checkbutton(server_frame,
                                   text="🖥️ Generate server .mrpack",
                                   variable=self.generate_server,
                                   style='TCheckbutton')
        server_cb.pack(anchor='w')
        
        server_desc = ttk.Label(server_frame,
                               text="   Only server-compatible mods and configs",
                               style='Subheading.TLabel',
                               font=('Segoe UI', 9))
        server_desc.pack(anchor='w', padx=(20, 0))
        
        # Overrides folder section
        overrides_section = ttk.Frame(section_frame)
        overrides_section.pack(fill='x', pady=(20, 0))
        
        ttk.Label(overrides_section, text="📂 Overrides Folder",
                 style='Heading.TLabel',
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        ttk.Label(overrides_section, text="Folder containing configs, resource packs, and other files",
                 style='Subheading.TLabel').pack(anchor='w', pady=(3, 10))
        
        overrides_entry = ttk.Entry(overrides_section, textvariable=self.overrides_folder,
                                   font=('Consolas', 10),
                                   style='TEntry')
        overrides_entry.pack(fill='x')
        
    def create_action_buttons(self, parent):
        """Create enhanced action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(0, 0))
        
        # Main update button with enhanced styling
        self.update_btn = ttk.Button(button_frame,
                                    text="🚀 Update Modpack",
                                    command=self.start_update,
                                    style='Accent.TButton')
        self.update_btn.pack(fill='x', pady=(0, 12))
        
        # Secondary buttons frame
        secondary_frame = ttk.Frame(button_frame)
        secondary_frame.pack(fill='x')
        
        # Stop button
        self.stop_btn = ttk.Button(secondary_frame,
                                  text="⏹️ Stop",
                                  command=self.stop_update,
                                  style='Secondary.TButton',
                                  state='disabled')
        self.stop_btn.pack(side='left', fill='x', expand=True, padx=(0, 6))
        
        # Clear output button
        clear_btn = ttk.Button(secondary_frame,
                              text="🗑️ Clear Log",
                              command=self.clear_output,
                              style='Secondary.TButton')
        clear_btn.pack(side='right', fill='x', expand=True, padx=(6, 0))
        
    def create_output_panel(self, parent):
        """Create the enhanced output panel"""
        output_frame = ttk.Frame(parent, style='Card.TFrame')
        
        # Panel header with enhanced styling
        header_frame = ttk.Frame(output_frame)
        header_frame.pack(fill='x', padx=25, pady=(20, 15))
        
        ttk.Label(header_frame, text="📋 Live Output", 
                 style='Heading.TLabel',
                 font=('Segoe UI', 13, 'bold')).pack(side='left')
        
        # Header buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side='right')
        
        # Output text area with enhanced styling
        output_container = ttk.Frame(output_frame)
        output_container.pack(fill='both', expand=True, padx=25, pady=(0, 20))
        
        # Create a frame for the text widget with border
        text_border_frame = tk.Frame(output_container, 
                                    bg=LunarBitTheme.BORDER, 
                                    bd=2, 
                                    relief='solid')
        text_border_frame.pack(fill='both', expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            text_border_frame,
            wrap=tk.WORD,
            bg=LunarBitTheme.SURFACE_VARIANT,
            fg=LunarBitTheme.TEXT_PRIMARY,
            insertbackground=LunarBitTheme.TEXT_PRIMARY,
            selectbackground=LunarBitTheme.PRIMARY,
            selectforeground=LunarBitTheme.TEXT_PRIMARY,
            font=('Cascadia Code', 10),  # Use a better monospace font
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=12
        )
        self.output_text.pack(fill='both', expand=True)
        
        # Enhanced progress bar
        progress_frame = ttk.Frame(output_container)
        progress_frame.pack(fill='x', pady=(15, 0))
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate', 
                                       style='TProgressbar')
        self.progress.pack(fill='x')
        
        # Status label
        self.status_label = ttk.Label(progress_frame, 
                                     text="Ready to update modpack",
                                     style='Subheading.TLabel',
                                     font=('Segoe UI', 9))
        self.status_label.pack(pady=(8, 0))
        
        return output_frame
        
    def browse_modpack(self):
        """Open file/folder browser for modpack selection with choice dialog"""
        current_path = self.modpack_path.get()
        initial_dir = os.path.dirname(current_path) if current_path else os.getcwd()
        
        # Create a custom dialog to choose between folder or file
        choice_window = tk.Toplevel(self.root)
        choice_window.title("Select Modpack Type")
        choice_window.geometry("400x200")
        choice_window.configure(bg=LunarBitTheme.BACKGROUND)
        choice_window.transient(self.root)
        choice_window.grab_set()
        
        # Center the dialog
        choice_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 250,
            self.root.winfo_rooty() + 200
        ))
        
        # Configure style for the dialog
        choice_frame = ttk.Frame(choice_window, style='Card.TFrame')
        choice_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(choice_frame, 
                               text="Choose Modpack Type",
                               style='Heading.TLabel',
                               font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(10, 15))
        
        # Description
        desc_label = ttk.Label(choice_frame,
                              text="What type of modpack would you like to select?",
                              style='Subheading.TLabel')
        desc_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = ttk.Frame(choice_frame)
        button_frame.pack(fill='x', pady=(0, 10))
        
        result = {'path': ''}
        
        def select_folder():
            choice_window.destroy()
            folder = filedialog.askdirectory(
                title="Select Modpack Folder",
                initialdir=initial_dir
            )
            if folder:
                result['path'] = folder
                
        def select_file():
            choice_window.destroy()
            file = filedialog.askopenfilename(
                title="Select .mrpack File",
                initialdir=initial_dir,
                filetypes=[("Modrinth Modpack", "*.mrpack"), ("All Files", "*.*")]
            )
            if file:
                result['path'] = file
                
        def cancel():
            choice_window.destroy()
        
        # Folder button
        folder_btn = ttk.Button(button_frame,
                               text="📁 Modpack Folder",
                               command=select_folder,
                               style='Accent.TButton')
        folder_btn.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        # File button  
        file_btn = ttk.Button(button_frame,
                             text="📦 .mrpack File", 
                             command=select_file,
                             style='Accent.TButton')
        file_btn.pack(side='right', expand=True, fill='x', padx=(5, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(choice_frame,
                               text="Cancel",
                               command=cancel,
                               style='Secondary.TButton')
        cancel_btn.pack(pady=(10, 0))
        
        # Wait for dialog to complete
        choice_window.wait_window()
        
        # Set the selected path
        if result['path']:
            self.modpack_path.set(result['path'])
            
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
        self.status_label.config(text="🚀 Starting modpack update...", 
                                foreground=LunarBitTheme.PRIMARY)
        
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
                    self.status_label.config(text="✅ Update completed!", 
                                           foreground=LunarBitTheme.SUCCESS)
                    break
                else:
                    # Add message to output
                    self.output_text.insert(tk.END, message)
                    self.output_text.see(tk.END)
                    
                    # Update status based on message content
                    if "Checking for mod updates" in message:
                        self.status_label.config(text="🔍 Checking for updates...", 
                                               foreground=LunarBitTheme.PRIMARY)
                    elif "Downloading" in message:
                        self.status_label.config(text="📥 Downloading updates...", 
                                               foreground=LunarBitTheme.PRIMARY)
                    elif "Generating" in message:
                        self.status_label.config(text="📦 Generating modpack...", 
                                               foreground=LunarBitTheme.PRIMARY)
                    elif "failed" in message.lower() or "error" in message.lower():
                        self.status_label.config(text="❌ Update failed!", 
                                               foreground=LunarBitTheme.SECONDARY)
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
