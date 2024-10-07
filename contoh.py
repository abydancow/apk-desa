from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class ClickableLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            print('Navigasi ke halaman pendaftaran')
            return True  # Mengindikasikan bahwa event telah ditangani
        return super().on_touch_down(touch)

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Label
        label = Label(text='Anda sudah memiliki akun?')
        layout.add_widget(label)

        # Label yang dapat diklik
        clickable_label = ClickableLabel(text='Belum memiliki akun? Klik di sini', color=(0, 0, 1, 1))  # Menggunakan warna biru
        layout.add_widget(clickable_label)

        return layout

if __name__ == '__main__':
    MyApp().run()
