from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder


# Config.set('graphics', 'width', '360')
# Config.set('graphics', 'height', '640')
# Config.set('graphics', 'resizable', False) 


class UserScreen(Screen):
    scroll_x_pos = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_scroll, 4)  # Mengatur interval setiap 4 detik

    def update_scroll(self, dt):
        scrollview = self.ids.my_scroll_view  # Mendapatkan ScrollView dari KV file
        if self.scroll_x_pos >= 1.0:  # Jika sudah sampai ujung kanan, kembali ke awal
            self.scroll_x_pos = 0.0
        else:
            self.scroll_x_pos += 0.5  # Mengatur kecepatan pengguliran
        scrollview.scroll_x = self.scroll_x_pos 

    def display_username(self, username):
        # Tampilkan username di label yang sesuai
        print("Username:", username)
        if username:  # Pastikan username tidak None
            self.ids.username_label.text = f"{username}"
        else:
            print("Username is None or empty!") 


# class UserApp(App):
#     def build(self):
#         kv_file_path = os.path.join(os.path.dirname(__file__), '..', 'kivy', 'user.kv')
#         Builder.load_file(kv_file_path)
#         return MyGrid()
    
# if __name__ =="__main__":
#     UserApp() .run()