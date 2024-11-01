import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.app import App

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
db = firebase.database()

# Model Artikel
class Article:
    def __init__(self, title, content, image):
        self.title = title
        self.content = content
        self.image = image

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'image': self.image
        }

# Layar CRUD
class ArticleScreen(Screen):
    title_input = ObjectProperty(None)
    content_input = ObjectProperty(None)
    image_input = ObjectProperty(None)
    selected_image_path = StringProperty("")  # Menggunakan StringProperty untuk binding

    def add_article(self):
        title = self.title_input.text
        content = self.content_input.text
        image = self.selected_image_path

        if title and content and image:
            article = Article(title, content, image)
            db.child("articles").push(article.to_dict())
            self.clear_inputs()
            self.load_articles()

    def load_articles(self):
        # Mengambil data dari Firebase
        self.ids.article_list.clear_widgets()
        articles = db.child("articles").get()

        for article in articles.each():
            title = article.val().get('title')
            content = article.val().get('content')
            image = article.val().get('image')
            self.ids.article_list.add_widget(
                Builder.load_string(f'''
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: "{title}"
                        Label:
                            text: "{content}"
                        Image:
                            source: "{image}"
                        Button:
                            text: "Edit"
                            on_press: app.root.get_screen('article').edit_article('{article.key}')
                        Button:
                            text: "Delete"
                            on_press: app.root.get_screen('article').delete_article('{article.key}')
                ''')
            )

    def clear_inputs(self):
        self.title_input.text = ''
        self.content_input.text = ''
        self.selected_image_path = ""  # Reset to empty string
        self.ids.image_input.text = ''  # Mengosongkan input gambar

    def edit_article(self, article_id):
        # Implementasi logika untuk mengedit artikel
        pass

    def delete_article(self, article_id):
        db.child("articles").child(article_id).remove()
        self.load_articles()

    def open_filechooser(self):
        content = FileChooserIconView()
        content.bind(on_submit=self.load_image)
        self.popup = Popup(title="Pilih Gambar", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def load_image(self, chooser, selection, touch):
        if selection:
            self.selected_image_path = selection[0]
            self.ids.image_input.text = self.selected_image_path
            self.popup.dismiss()