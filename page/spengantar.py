import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from storage import StorageManager
from database import FirebaseDB
from tenacity import retry, stop_after_attempt, wait_fixed
import os

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from database import FirebaseDB
from tenacity import retry, stop_after_attempt, wait_fixed

class Database(FirebaseDB):
    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get_all_spengantars():
        try:
            spengantars = FirebaseDB.db.child("spengantars").get()
            if spengantars.each():
                return [(spengantar.key(), spengantar.val()) for spengantar in spengantars.each()]
            return []
        except Exception as e:
            print(f"Error getting spengantars: {e}")
            return []

class SpengantarItem(BoxLayout):
    def __init__(self, spengantar_id, spengantar_data, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50  # Menampilkan hanya nama
        self.padding = 5
        self.spacing = 10

        self.spengantar_id = spengantar_id
        self.spengantar_data = spengantar_data
        self.screen_manager = screen_manager  # Mengakses screen_manager dari App

        # Label Nama
        name = spengantar_data.get('nama', 'No Name')
        name_label = Label(
            text=name,
            size_hint_x=0.7,
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        # Tombol Show untuk membuka detail screen
        show_btn = Button(
            text="Show",
            size_hint_x=0.3,
            background_color=(0.3, 0.5, 0.9, 1)
        )
        show_btn.bind(on_press=self.show_details)

        # Tambahkan komponen ke layout
        self.add_widget(name_label)
        self.add_widget(show_btn)

    def show_details(self, instance):
        # Pindah ke SpengantarDetailScreen dengan data yang ada
        detail_screen = self.screen_manager.get_screen('spengantar_detail')
        detail_screen.display_details(self.spengantar_data)
        self.screen_manager.current = 'spengantar_detail'

class SpengantarList(Screen):
    container = ObjectProperty(None)
    screen_manager = ObjectProperty(None)  # Menambahkan screen_manager untuk komunikasi antar layar
    
    def on_enter(self):
        self.load_spengantars()
    
    def load_spengantars(self):
        self.container.clear_widgets()
        spengantars = Database.get_all_spengantars()
        
        if spengantars:
            for spengantar_id, spengantar_data in spengantars:
                spengantar_item = SpengantarItem(
                    spengantar_id,
                    spengantar_data,
                    self.manager  # Mengirimkan manager (ScreenManager) yang ada
                )
                self.container.add_widget(spengantar_item)
        else:
            self.container.add_widget(
                Label(
                    text="Tidak ada produk tersedia",
                    size_hint_y=None,
                    height=100
                )
            )

class SpengantarDetailScreen(Screen):
    detail_label = ObjectProperty(None)
    ktp_image = ObjectProperty(None)
    kk_image = ObjectProperty(None)
    
    def display_details(self, spengantar_data):
        # Menampilkan detail informasi di layar detail
        if self.detail_label is not None:
            name = spengantar_data.get('nama', 'No Name')
            keperluan = spengantar_data.get('keperluan', 'No Keperluan')
            
            detail_text = f"Nama: {name}\nKeperluan: {keperluan}\n"
            self.detail_label.text = detail_text
        else:
            print("detail_label belum terinisialisasi")

        # Menampilkan gambar KTP
        ktp_image_url = spengantar_data.get('ktp_image_url', None)
        if ktp_image_url:
            self.ktp_image.source = ktp_image_url
        else:
            self.ktp_image.source = ''  # Kosongkan jika tidak ada gambar

        # Menampilkan gambar KK
        kk_image_url = spengantar_data.get('kk_image_url', None)
        if kk_image_url:
            self.kk_image.source = kk_image_url
        else:
            self.kk_image.source = ''  # Kosongkan jika tidak ada gambar

    def acc_action(self):
        # Logika untuk tindakan ACC
        print("Surat pengantar di-ACC")
        # Tambahkan logika yang dibutuhkan untuk "ACC", seperti memperbarui status di database.

    def revisi_action(self):
        # Logika untuk tindakan Revisi
        print("Surat pengantar diminta revisi")
        # Tambahkan logika yang dibutuhkan untuk "Revisi", seperti mengirim pesan ke user untuk revisi.
   
class ImageChooserPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Pilih Gambar'
        self.size_hint = (0.9, 0.9)
        self.callback = callback

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.file_chooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path='.')
        layout.add_widget(self.file_chooser)

        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        
        cancel_btn = Button(text='Batal')
        cancel_btn.bind(on_press=self.dismiss)
        
        select_btn = Button(text='Pilih', background_color=(0.3, 0.5, 0.9, 1))
        select_btn.bind(on_press=self.select_image)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(select_btn)
        
        layout.add_widget(button_layout)
        self.content = layout

    def select_image(self, instance):
        if self.file_chooser.selection:
            self.callback(self.file_chooser.selection[0])
            self.dismiss()
