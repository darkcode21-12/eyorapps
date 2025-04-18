import customtkinter as ctk
from tkinter import messagebox
import socket
import json
import winsound  

SERVER_HOST = '192.168.1.100'  # IP of the server
SERVER_PORT = 9000

class StudentApp:
    def __init__(self, master):
        self.master = master
        self.master.title("👩‍🎓 Student Dashboard")
        self.master.geometry("500x400")
        
        # Set custom appearance (you can customize this further)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Login Form
        self.student_id_label = ctk.CTkLabel(master, text="Student ID", font=("Arial", 14))
        self.student_id_label.pack(pady=5)

        self.student_id_entry = ctk.CTkEntry(master, width=250)
        self.student_id_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(master, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.notifications_listbox = ctk.CTkTextbox(master, height=10, width=50)
        self.notifications_listbox.pack(pady=10, fill=ctk.BOTH, expand=True)

    def login(self):
        student_id = self.student_id_entry.get()
        data = {"student_id": student_id}
        self.send_to_server("GET_STUDENT", data)

    def send_to_server(self, command, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_HOST, SERVER_PORT))
                payload = f"{command}|{json.dumps(data)}"
                s.send(payload.encode())

                # Receive response from server
                response = s.recv(8192).decode()
                self.handle_server_response(response)

        except Exception as e:
            print("[SERVER ERROR]", e)

    def handle_server_response(self, response):
        try:
            data = json.loads(response)

            if data.get("error"):
                messagebox.showerror("Error", data["error"])
            elif data.get("message"):
                messagebox.showinfo("Success", data["message"])
            elif "notifications" in data:
                self.show_notifications(data["notifications"])
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid response from server.")

    def show_notifications(self, notifications):
        if notifications:
            for notification in notifications:
                message = f"Message: {notification['message']}\nHomework: {notification['homework']}"
                self.notifications_listbox.insert(ctk.END, message)
                
                # Play system notification sound
                winsound.Beep(1000, 500)  # Simple beep sound

                # Ask server to mark notification as read
                notification_index = len(self.notifications_listbox.get(0, ctk.END)) - 1
                data = {"student_id": self.student_id_entry.get(), "notification_index": notification_index}
                self.send_to_server("MARK_AS_READ", data)
        else:
            self.notifications_listbox.insert(ctk.END, "No unread notifications.")

if __name__ == '__main__':
    root = ctk.CTk()  # Use CTk for CustomTkinter window
    app = StudentApp(root)
    root.mainloop()
