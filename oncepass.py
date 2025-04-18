import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import uuid
import socket
import json
import random

ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

SERVER_HOST = '192.168.1.100'
SERVER_PORT = 9000

class CreateAccountApp:
    def __init__(self, master):
        self.master = master
        self.master.title("📘 Create Account")
        self.master.geometry("550x580")

        self.tab_control = ctk.CTkTabview(self.master, width=500, height=500)
        self.tab_control.pack(pady=20)

        self.student_tab = self.tab_control.add("Student")
        self.parent_tab = self.tab_control.add("Parent")

        self.build_student_tab()
        self.build_parent_tab()

    def build_student_tab(self):
        ctk.CTkLabel(self.student_tab, text="Student Registration", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.student_name = ctk.CTkEntry(self.student_tab, width=250, placeholder_text="Full Name")
        self.student_name.pack(pady=10)

        self.focus_mode = ctk.BooleanVar()
        ctk.CTkCheckBox(self.student_tab, text="🔕 Focus Mode (Silence Notifications)", variable=self.focus_mode).pack(pady=5)

        self.captcha_code = str(random.randint(1000, 9999))
        ctk.CTkLabel(self.student_tab, text=f"CAPTCHA: {self.captcha_code}", font=ctk.CTkFont(size=14)).pack(pady=5)
        self.captcha_input = ctk.CTkEntry(self.student_tab, width=100, placeholder_text="Enter CAPTCHA")
        self.captcha_input.pack(pady=5)

        ctk.CTkButton(self.student_tab, text="🎓 Create Student Account", command=self.create_student_account).pack(pady=20)

    def build_parent_tab(self):
        ctk.CTkLabel(self.parent_tab, text="Parent Registration", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.parent_name = ctk.CTkEntry(self.parent_tab, width=250, placeholder_text="Parent Name")
        self.parent_name.pack(pady=10)

        self.parent_pic_path = None
        ctk.CTkButton(self.parent_tab, text="📸 Upload Profile Picture", command=self.upload_profile_pic).pack(pady=10)
        self.profile_preview = ctk.CTkLabel(self.parent_tab, text="")
        self.profile_preview.pack(pady=10)

        ctk.CTkButton(self.parent_tab, text="👪 Create Parent Account", command=self.create_parent_account).pack(pady=20)

    def upload_profile_pic(self):
        file_path = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.parent_pic_path = file_path
            img = Image.open(file_path).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            self.profile_preview.configure(image=img_tk, text="")
            self.profile_preview.image = img_tk

    def send_to_server(self, payload, mode):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_HOST, SERVER_PORT))
                s.send(f"{mode}|{json.dumps(payload)}".encode())
                response = s.recv(1024)
                return response.decode()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
            return None

    def create_student_account(self):
        if self.captcha_input.get() != self.captcha_code:
            messagebox.showerror("CAPTCHA Failed", "CAPTCHA incorrect. Please try again.")
            return

        sid = str(uuid.uuid4())[:8]
        data = {
            'student_id': sid,
            'name': self.student_name.get(),
            'focus_mode': self.focus_mode.get()
        }
        result = self.send_to_server(data, 'CREATE_STUDENT')
        if result == 'STUDENT_SAVED':
            messagebox.showinfo("Success", f"Account created! Your ID: {sid}")
        else:
            messagebox.showerror("Failed", "Account creation failed.")

    def create_parent_account(self):
        pid = str(uuid.uuid4())[:8]
        data = {
            'parent_id': pid,
            'name': self.parent_name.get(),
            'profile_picture': self.parent_pic_path or ""
        }
        result = self.send_to_server(data, 'CREATE_PARENT')
        if result == 'PARENT_SAVED':
            messagebox.showinfo("Success", f"Parent account created! ID: {pid}")
        else:
            messagebox.showerror("Failed", "Could not save parent data.")

if __name__ == '__main__':
    root = ctk.CTk()
    app = CreateAccountApp(root)
    root.mainloop()
