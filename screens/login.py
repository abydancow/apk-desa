import pyrebase
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

firebase_config = {
    "apiKey": "AIzaSyDcPf3IXEcInnLVLGSfo9b2pgyNsfn_CqI",
    "authDomain": "apk-desa-cfcf3.firebaseapp.com",
    "databaseURL": "https://apk-desa-cfcf3-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "apk-desa-cfcf3",
    "storageBucket": "apk-desa-cfcf3.appspot.com",
    "messagingSenderId": "520440091443",
    "appId": "1:520440091443:android:ac6dcc378e056989f42446"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()  
db = firebase.database() 

class LoginScreen(Screen):
    def login(self):
        email = self.ids.email_input.text  
        password = self.ids.password_input.text  

        # Validasi input
        if not email or not password:
            self.show_popup("Error", "Semua kolom harus diisi!")
            return

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # Simpan email di App
            self.manager.user_email = email  
            user_id = user['localId']  
            user_data = db.child("users").child(user_id).get().val()
            print("User Data:", user_data)
            role = user_data.get('role')  
            username = user_data.get('username')
            print("Username:", username)  

            # Pindah ke layar UserScreen
            self.manager.current = 'user'
            user_screen = self.manager.get_screen('user')  
            user_screen.display_username(username)
            

            if role == 'admin':
                self.manager.current = 'admin'  
            elif role == 'user':
                self.manager.current = 'user'  
            else:
                self.show_popup("Error", "Role tidak dikenal.")
        except Exception as e:
            self.show_popup("Error", str(e))  

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.3))
        popup.open()