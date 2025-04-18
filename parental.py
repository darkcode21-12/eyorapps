from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
import json
import os
from PIL import Image as PILImage

PROFILE_DIR = 'parents'
CHILD_PROFILES_DIR = 'children'  # Directory to store child profiles
os.makedirs(PROFILE_DIR, exist_ok=True)
os.makedirs(CHILD_PROFILES_DIR, exist_ok=True)

class ParentApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.tabs = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Tabs
        self.login_tab = Button(text="Login")
        self.create_tab = Button(text="Create Account")
        self.login_tab.bind(on_press=self.show_login_tab)
        self.create_tab.bind(on_press=self.show_create_tab)
        self.tabs.add_widget(self.login_tab)
        self.tabs.add_widget(self.create_tab)

        self.root.add_widget(self.tabs)

        # Create Account Fields (default view)
        self.create_account_layout = BoxLayout(orientation='vertical')
        self.name_input = TextInput(hint_text="Parent Name", size_hint_y=None, height=40)
        self.parent_id_input = TextInput(hint_text="Parent ID", size_hint_y=None, height=40)
        self.create_account_layout.add_widget(self.name_input)
        self.create_account_layout.add_widget(self.parent_id_input)

        self.create_button = Button(text="Create Account", size_hint_y=None, height=50)
        self.create_button.bind(on_press=self.create_account)
        self.create_account_layout.add_widget(self.create_button)

        # Login Fields (default view)
        self.login_layout = BoxLayout(orientation='vertical')
        self.login_id_input = TextInput(hint_text="Parent ID", size_hint_y=None, height=40)
        self.login_layout.add_widget(self.login_id_input)

        self.login_button = Button(text="Login", size_hint_y=None, height=50)
        self.login_button.bind(on_press=self.login)
        self.login_layout.add_widget(self.login_button)

        self.root.add_widget(self.login_layout)
        self.root.add_widget(self.create_account_layout)

        return self.root

    def show_login_tab(self, instance):
        self.create_account_layout.clear_widgets()
        self.create_account_layout.add_widget(self.name_input)
        self.create_account_layout.add_widget(self.parent_id_input)

    def show_create_tab(self, instance):
        self.login_layout.clear_widgets()
        self.login_layout.add_widget(self.login_id_input)

    def create_account(self, instance):
        name = self.name_input.text
        pid = self.parent_id_input.text
        if not name or not pid:
            self.show_error_popup("All fields must be filled.")
            return

        data = {
            "name": name,
            "parent_id": pid
        }
        with open(os.path.join(PROFILE_DIR, f"{pid}.json"), 'w') as f:
            json.dump(data, f)
        self.show_success_popup("Account Created", "Parent account created successfully!")

    def login(self, instance):
        pid = self.login_id_input.text
        profile_path = os.path.join(PROFILE_DIR, f"{pid}.json")
        if not os.path.exists(profile_path):
            self.show_error_popup("Login Failed", "Parent ID not found.")
            return

        with open(profile_path) as f:
            data = json.load(f)

        self.open_dashboard(data)

    def open_dashboard(self, data):
        dashboard = BoxLayout(orientation='vertical')
        dashboard.add_widget(Label(text=f"Welcome, {data['name']}", font_size=20))

        dashboard.add_widget(Button(text="Add Child Profile"))

        self.root.clear_widgets()
        self.root.add_widget(dashboard)

    def show_error_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_success_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    ParentApp().run()
