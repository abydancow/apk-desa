from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color

class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Mengatur warna latar belakang halaman
        with self.canvas.before:
            Color(0.2, 0.4, 0.6, 1)  # Warna biru tua untuk latar belakang
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Judul di atas logo
        self.title_label = Label(text="KELURAHAN DESA SANGGUNG", font_size=32, bold=True,
                                 size_hint=(None, None), color=(1, 1, 1, 1),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.85})
        self.add_widget(self.title_label)

        # Logo di tengah atas
        self.logo = Image(source='logo.png', size_hint=(None, None), size=(150, 150),
                          pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(self.logo)

        # Layout vertikal untuk username, password, dan tombol login
        self.form_layout = BoxLayout(orientation='vertical', size_hint=(0.8, 0.4),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.3})

        # Label dan input Username
        self.username_label = Label(text="Username", size_hint_y=None, height=40, color=(1, 1, 1, 1))
        self.form_layout.add_widget(self.username_label)
        self.username_input = TextInput(hint_text='Masukkan username', multiline=False,
                                        background_color=(0.7, 0.7, 0.9, 1), foreground_color=(0, 0, 0, 1))   
        self.form_layout.add_widget(self.username_input)
      
        # Label dan input Password
        self.password_label = Label(text="Password", size_hint_y=None, height=40, color=(1, 1, 1, 1))
        self.form_layout.add_widget(self.password_label)
        self.password_input = TextInput(hint_text='Masukkan password', password=True, multiline=False,
                                        background_color=(0.7, 0.7, 0.9, 1), foreground_color=(0, 0, 0, 1))
        self.form_layout.add_widget(self.password_input)
      
        # Tombol Login
        self.login_button = Button(text='Login', size_hint_y=None, height=50,
                                   background_color=(0.1, 0.6, 0.2, 1),  # Warna hijau untuk tombol
                                   color=(1, 1, 1, 1))  # Teks putih pada tombol
        self.form_layout.add_widget(self.login_button)
      
        # Tambahkan form layout ke FloatLayout
        self.add_widget(self.form_layout)

    # Fungsi untuk memperbarui latar belakang saat ukuran berubah
    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MyApp(App):
    def build(self):
        return LoginScreen()
    
if __name__ == '__main__':
    MyApp().run()
