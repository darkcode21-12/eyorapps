# installer_app.py
import sys
import os
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import requests
import subprocess
import shutil
import customtkinter as ctk

# Constants
GITHUB_URL = "https://github.com/your-org/your-project/releases/download/v1.0/"
FILES = {
    "Teacher": "installer-teacher.zip",
    "Student": "installer-student.zip"
}

# Globals
theme = "light"

# Splash screen
class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.overrideredirect(True)
        self.configure(fg_color="#1e1e2e")
        self.geometry("400x250+500+300")
        label = ctk.CTkLabel(self, text="🚀 Eyor Installer", font=("Segoe UI", 24, "bold"), text_color="#cdd6f4")
        label.pack(expand=True)
        subtitle = ctk.CTkLabel(self, text="Loading...", font=("Segoe UI", 14, "italic"), text_color="#a6adc8")
        subtitle.pack()
        self.after(3000, self.destroy)

# Main Installer UI
class InstallerApp(ctk.CTk):
    def __init__(self, silent=False):
        super().__init__()
        self.title("Eyor Installer")
        self.geometry("650x550")
        self.silent = silent
        self.download_dir = tk.StringVar(value=os.getcwd())
        self.set_theme("light")
        self.create_widgets()

        if not silent:
            self.show_license_page()
        else:
            self.start_installation("Student")

    def set_theme(self, mode):
        global theme
        theme = mode
        ctk.set_appearance_mode("Dark" if mode == "dark" else "Light")

    def toggle_theme(self):
        self.set_theme("dark" if theme == "light" else "light")

    def create_widgets(self):
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=30)

        self.role_var = tk.StringVar(value="Student")
        ctk.CTkLabel(self, text="Select Role:").pack()
        self.role_combo = ctk.CTkComboBox(self, values=["Student", "Teacher"], variable=self.role_var)
        self.role_combo.pack(pady=5)

        ctk.CTkLabel(self, text="Choose Download Location:").pack(pady=5)
        self.path_entry = ctk.CTkEntry(self, textvariable=self.download_dir, width=400)
        self.path_entry.pack(pady=5)
        ctk.CTkButton(self, text="Browse", command=self.browse_directory).pack()

        ctk.CTkButton(self, text="Start Installation", command=self.on_start).pack(pady=10)
        ctk.CTkButton(self, text="Toggle Theme", command=self.toggle_theme).pack(pady=10)

    def browse_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.download_dir.set(selected_dir)

    def on_start(self):
        self.show_license_page()

    def show_license_page(self):
        license_window = ctk.CTkToplevel(self)
        license_window.title("License Agreement")
        license_window.geometry("500x350")
        text = tk.Text(license_window, wrap="word")
        text.insert("1.0", "LICENSE AGREEMENT:\n\nBy continuing, you agree to our terms...")
        text.pack(expand=True, fill="both")
        ctk.CTkButton(license_window, text="Accept", command=lambda: [license_window.destroy(), self.start_installation(self.role_var.get())]).pack(pady=10)

    def start_installation(self, role):
        threading.Thread(target=self.download_and_install, args=(role,), daemon=True).start()

    def download_and_install(self, role):
        filename = FILES[role]
        url = GITHUB_URL + filename
        dest = os.path.join(self.download_dir.get(), filename)

        self.progress.set(0)
        self.update_idletasks()

        response = requests.get(url, stream=True)
        total = int(response.headers.get("content-length", 0))
        with open(dest, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    self.progress.set(downloaded / total)
                    self.update_idletasks()

        if sys.platform.startswith("win"):
            self.create_start_menu_shortcut()

        messagebox.showinfo("Done", "Installation Complete!")

    def create_start_menu_shortcut(self):
        try:
            import winshell
            from win32com.client import Dispatch
            shortcut_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Eyor Installer.lnk")
            target = os.path.join(os.getcwd(), "your_installed_app.exe")
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.IconLocation = target
            shortcut.save()
        except Exception as e:
            print("Failed to create shortcut:", e)

if __name__ == "__main__":
    silent_mode = "--silent" in sys.argv
    app = InstallerApp(silent=silent_mode)
    splash = SplashScreen(app)
    app.withdraw()
    app.after(3000, lambda: [splash.destroy(), app.deiconify()])
    app.mainloop()
