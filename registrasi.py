from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle

class ClickableLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            print('Navigasi ke halaman registrasi')
            return True
        return super().on_touch_down(touch)

class LineTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_line, pos=self._update_line)

    def _update_line(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Warna garis (hitam)
            Line(points=[self.x, self.y, self.x + self.width, self.y], width=1)

class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Mengatur warna latar belakang halaman
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Warna latar belakang putih
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Judul di atas logo
        self.title_label = Label(text="KELURAHAN DESA SANGGUNG", font_size=32, bold=True,
                                 size_hint=(None, None), color=(0, 0, 0, 1),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.85})
        self.add_widget(self.title_label)

        # Logo di tengah atas
        self.logo = Image(source='img/1.jpg', size_hint=(None, None), size=(400, 250),
                          pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.add_widget(self.logo)

        # Layout vertikal untuk username, password, dan tombol login
        self.form_layout = BoxLayout(orientation='vertical', size_hint=(0.8, 0.4),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.3})

        # Label dan input Username
        self.username_input = LineTextInput(hint_text='Masukkan username', multiline=False,
                                        background_color=(1, 1, 1, 0),  # Transparan
                                        foreground_color=(0, 0, 0, 1),
                                        size_hint=(0.8, None), height=40,
                                        pos_hint={'center_x': 0.5})   
        self.form_layout.add_widget(self.username_input)
        self.form_layout.add_widget(Label(size_hint_y=None, height=10))  # Spacer

        # Label dan input NIK (hanya angka)
        self.NIK_input = LineTextInput(hint_text='Masukkan NIK', multiline=False,
                                        background_color=(1, 1, 1, 0),
                                        foreground_color=(0, 0, 0, 1),
                                        size_hint=(0.8, None), height=40,
                                        pos_hint={'center_x': 0.5},
                                        input_filter='int')  # Hanya menerima angka
        self.form_layout.add_widget(self.NIK_input)
        self.form_layout.add_widget(Label(size_hint_y=None, height=10))  # Spacer

        # Label dan input Email (memiliki @)
        self.Email_input = LineTextInput(hint_text='Masukkan email', multiline=False,
                                        background_color=(1, 1, 1, 0),
                                        foreground_color=(0, 0, 0, 1),
                                        size_hint=(0.8, None), height=40,
                                        pos_hint={'center_x': 0.5})   
        self.form_layout.add_widget(self.Email_input)
        self.form_layout.add_widget(Label(size_hint_y=None, height=10))  # Spacer

        # Label dan input Password
        self.password_input = LineTextInput(hint_text='Masukkan password', password=True, multiline=False,
                                        background_color=(1, 1, 1, 0),
                                        foreground_color=(0, 0, 0, 1),
                                        size_hint=(0.8, None), height=40,
                                        pos_hint={'center_x': 0.5})
        self.form_layout.add_widget(self.password_input)
        self.form_layout.add_widget(Label(size_hint_y=None, height=50))  # Spacer

        # Tombol Login
        self.Registrasi_button = Button(text='Registrasi', size_hint=(0.4, None), height=40,
                                   pos_hint={'center_x': 0.5},
                                   background_color=(0.1, 0.6, 0.2, 1),
                                   color=(1, 1, 1, 1))
        self.form_layout.add_widget(self.Registrasi_button)


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
