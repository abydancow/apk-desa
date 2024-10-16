import pyrebase
from kivy.uix.screenmanager import Screen

# Konfigurasi Firebase
firebase_config = {
    "apiKey": "AIzaSyDcPf3IXEcInnLVLGSfo9b2pgyNsfn_CqI",
    "authDomain": "apk-desa-cfcf3.firebaseapp.com",
    "databaseURL": "https://apk-desa-cfcf3-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "apk-desa-cfcf3",
    "storageBucket": "apk-desa-cfcf3.appspot.com",
    "messagingSenderId": "520440091443",
    "appId": "1:520440091443:android:ac6dcc378e056989f42446"
}

# Inisialisasi Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()  # Inisialisasi auth
db = firebase.database()  # Inisialisasi database


class RegistrasiScreen(Screen):
    def register_user(self):
        username = self.ids.username.text
        nik = self.ids.nik.text
        email = self.ids.email.text
        password = self.ids.password.text
        role = "user"    

        # Validasi input
        if not username or not nik or not email or not password:
            self.show_popup("Error", "Semua kolom harus diisi!")
            return

        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']  

            user_data = {
                "user_id": user_id,
                "username": username,
                "email": email,
                "nik": nik,
                "role": role  
            }
            db.child("users").child(user_id).set(user_data)

            self.ids.username.text = ""
            self.ids.nik.text = ""
            self.ids.email.text = ""
            self.ids.password.text = ""

            self.manager.current = 'login'

        except Exception as e:
            self.show_popup("Error", str(e))  
