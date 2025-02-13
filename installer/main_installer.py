import tkinter as tk
from tkinter import messagebox, ttk
import json
import threading
import time
import os
import sys

from install_utils import install_tool, validate_installation
from cleanup import cleanup_files

class InstallerGUI(tk.Tk):
    def __init__(self, config):
        super().__init__()
        self.title("Forensic Tools Installer")
        self.geometry("500x400")
        self.resizable(False, False)
        self.config_data = config
        self.selected_tools = {}
        self.create_main_menu()

    def create_main_menu(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        header = tk.Label(self, text="Welcome to the Forensic Tools Installer!", font=("Arial", 16))
        header.pack(pady=20)

        subheader = tk.Label(self, text="Choose an installation option:", font=("Arial", 12))
        subheader.pack(pady=10)

        tk.Button(self, text="Full Installation", font=("Arial", 12), width=25, command=self.full_installation).pack(pady=10)
        tk.Button(self, text="Selective Installation", font=("Arial", 12), width=25, command=self.selective_installation).pack(pady=10)

    def full_installation(self):
        # Mark all tools as selected
        self.selected_tools = { key: True for key in self.config_data["tools"].keys() }
        self.start_installation()

    def selective_installation(self):
        # Clear window for tool selection checklist
        for widget in self.winfo_children():
            widget.destroy()
        
        header = tk.Label(self, text="Select the tools to install:", font=("Arial", 14))
        header.pack(pady=10)

        self.check_vars = {}
        checklist_frame = tk.Frame(self)
        checklist_frame.pack(pady=10)

        # Create a checkbox for each tool defined in config
        for key, tool in self.config_data["tools"].items():
            var = tk.BooleanVar(value=False)
            tk.Checkbutton(checklist_frame, text=tool["name"], variable=var, font=("Arial", 12)).pack(anchor='w', padx=20, pady=5)
            self.check_vars[key] = var

        tk.Button(self, text="Proceed", font=("Arial", 12), width=20, command=self.collect_selection).pack(pady=20)

    def collect_selection(self):
        # Gather user selections from checkboxes
        self.selected_tools = { key: var.get() for key, var in self.check_vars.items() }
        if not any(self.selected_tools.values()):
            messagebox.showwarning("No Selection", "Please select at least one tool to install.")
        else:
            self.start_installation()

    def start_installation(self):
        # Clear the window and set up the installation progress screen
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Installing selected tools...", font=("Arial", 14)).pack(pady=10)
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=20)
        self.status_label = tk.Label(self, text="Starting installation...", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # Run installation in a separate thread to keep the GUI responsive
        threading.Thread(target=self.run_installation, daemon=True).start()

    def run_installation(self):
        total = sum(1 for selected in self.selected_tools.values() if selected)
        if total == 0:
            self.status_label.config(text="No tools selected. Exiting.")
            return

        count = 0
        for key, selected in self.selected_tools.items():
            if selected:
                tool = self.config_data["tools"][key]
                self.status_label.config(text=f"Installing {tool['name']}...")
                self.update_idletasks()

                # Run installation routine
                success = install_tool(tool)
                if success and validate_installation(tool):
                    status = f"{tool['name']} installed successfully."
                else:
                    status = f"Error installing {tool['name']}."
                self.status_label.config(text=status)
                time.sleep(1)  # Brief pause for user to read status message
                count += 1
                self.progress['value'] = (count / total) * 100
                self.update_idletasks()

        self.status_label.config(text="Installation complete! Cleaning up...")
        time.sleep(1)
        cleanup_files()  # Execute cleanup routine
        self.status_label.config(text="Cleanup complete. Closing installer...")
        time.sleep(1)
        self.quit()

def main():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
    except Exception as e:
        messagebox.showerror("Configuration Error", f"Failed to load config.json: {e}")
        sys.exit(1)

    app = InstallerGUI(config)
    app.mainloop()

if __name__ == "__main__":
    main()

