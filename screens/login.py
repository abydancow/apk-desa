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
        email = self.ids.email_input.text  # Ambil email dari input
        password = self.ids.password_input.text  # Ambil password dari input

        # Validasi input
        if not email or not password:
            self.show_popup("Error", "Semua kolom harus diisi!")
            return

        try:
            # Login ke Firebase Authentication
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = user['localId']  # Mendapatkan UID pengguna
            user_data = db.child("users").child(user_id).get().val()
            print("User Data:", user_data)
            role = user_data.get('role')  # Mendapatkan role dari pengguna
            username = user_data.get('username')
            print("Username:", username)  # Debug: Pastikan username berhasil diambil

            # Pindah ke layar UserScreen
            self.manager.current = 'user'
            user_screen = self.manager.get_screen('user')  # Ambil instance UserScreen
            user_screen.display_username(username)
            

            # Arahkan ke halaman yang sesuai berdasarkan role
            if role == 'admin':
                self.manager.current = 'admin'  # Ganti ke layar admin
            elif role == 'user':
                self.manager.current = 'user'  # Ganti ke layar user
            else:
                self.show_popup("Error", "Role tidak dikenal.")
        except Exception as e:
            self.show_popup("Error", str(e))  # Menampilkan kesalahan dalam popup

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.3))
        popup.open()