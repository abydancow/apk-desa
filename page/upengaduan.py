from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

class UpengaduanScreen(Screen):
    def __init__(self, **kwargs):
        super(UpengaduanScreen, self).__init__(**kwargs)

        # Pilihan untuk tombol pertama
        self.options_1 = [
            'Administrasi dan Tata Kelola',
            'Sosial dan Masyarakat',
            'Infrastruktur',
            'Lainnya'
        ]
        self.current_option_index_1 = 0

        # Pilihan untuk tombol kedua
        self.options_2 = [
            'Ringan',
            'Sedang',
            'Berat'
        ]
        self.current_option_index_2 = 0

    def change_option_1(self, button):
        # Ubah teks tombol pertama berdasarkan pilihan berikutnya
        self.current_option_index_1 = (self.current_option_index_1 + 1) % len(self.options_1)
        button.text = self.options_1[self.current_option_index_1]

    def change_option_2(self, button):
        # Ubah teks tombol kedua berdasarkan pilihan berikutnya
        self.current_option_index_2 = (self.current_option_index_2 + 1) % len(self.options_2)
        button.text = self.options_2[self.current_option_index_2]