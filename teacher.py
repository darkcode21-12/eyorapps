import customtkinter as ctk
from tkinter import messagebox
import socket
import json

SERVER_HOST = '192.168.1.100'  # IP of the server
SERVER_PORT = 9000

root=ctk.CTk()

ctk.set_appearance_mode("System")  # "Dark", "Light", or "System"
ctk.set_default_color_theme("green")  # "blue", "green", etc.
root.iconbitmap(r"A:\eyor web\clinetapp\student_homework\school.ico")  


class TeacherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("👨‍🏫 Teacher Dashboard")
        self.master.geometry("520x460")

        ctk.CTkLabel(master, text="Search for Student by ID", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        self.student_id_entry = ctk.CTkEntry(master, width=250, placeholder_text="Enter Student ID")
        self.student_id_entry.pack(pady=5)

        ctk.CTkButton(master, text="🔍 Search", command=self.search_student).pack(pady=10)

        ctk.CTkLabel(master, text="📢 Message to Publish to All Students", font=ctk.CTkFont(size=14)).pack(pady=10)
        self.message_entry = ctk.CTkEntry(master, width=350, placeholder_text="Type your announcement here...")
        self.message_entry.pack(pady=5)

        ctk.CTkButton(master, text="📤 Publish to All", command=self.publish_to_all).pack(pady=15)

    def search_student(self):
        student_id = self.student_id_entry.get()
        data = {"student_id": student_id}
        self.send_to_server("GET_STUDENT", data)

    def publish_to_all(self):
        message = self.message_entry.get()
        if message.strip() == "":
            messagebox.showwarning("Empty Message", "Please enter a message to publish.")
            return
        data = {"message": message}
        self.send_to_server("PUBLISH_TO_ALL", data)

    def send_to_server(self, command, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_HOST, SERVER_PORT))
                payload = f"{command}|{json.dumps(data)}"
                s.send(payload.encode())
                response = s.recv(8192).decode()
                self.handle_server_response(response)
        except Exception as e:
            print("[SERVER ERROR]", e)
            messagebox.showerror("Connection Error", str(e))

    def handle_server_response(self, response):
        try:
            data = json.loads(response)
            if data.get("error"):
                messagebox.showerror("Error", data["error"])
            elif data.get("message"):
                messagebox.showinfo("Success", data["message"])
            else:
                self.display_student_info(data)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid response from server.")

    def display_student_info(self, data):
        dashboard = ctk.CTkToplevel(self.master)
        dashboard.title(f"🎓 Student: {data['name']}")
        dashboard.geometry("400x250")

        ctk.CTkLabel(dashboard, text=f"Name: {data['name']}", font=ctk.CTkFont(size=18)).pack(pady=15)
        ctk.CTkLabel(dashboard, text=f"Student ID: {data['student_id']}", font=ctk.CTkFont(size=14)).pack(pady=10)

        if data.get('focus_mode'):
            ctk.CTkLabel(dashboard, text="Focus Mode: Enabled 🔕", text_color="green").pack(pady=5)
        else:
            ctk.CTkLabel(dashboard, text="Focus Mode: Disabled 🔔", text_color="gray").pack(pady=5)

if __name__ == '__main__':
    root = ctk.CTk()
    app = TeacherApp(root)
    root.mainloop()
