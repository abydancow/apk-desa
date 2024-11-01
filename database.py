import pyrebase
from config import get_firebase_config

class FirebaseDB:
    config = get_firebase_config()
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
