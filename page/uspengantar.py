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

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def add_spengantar(spengantar_data):
        try:
            return FirebaseDB.db.child("spengantars").push(spengantar_data)
        except Exception as e:
            print(f"Error adding spengantar: {e}")
            raise e

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def update_spengantar(spengantar_id, spengantar_data):
        try:
            return FirebaseDB.db.child("spengantars").child(spengantar_id).update(spengantar_data)
        except Exception as e:
            print(f"Error updating spengantar: {e}")
            raise e

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def delete_spengantar(spengantar_id):
        try:
            return FirebaseDB.db.child("spengantars").child(spengantar_id).remove()
        except Exception as e:
            print(f"Error deleting spengantar: {e}")
            raise e
        
class AddUspengantar(Screen):
    name_input = ObjectProperty(None)
    keperluan_input = ObjectProperty(None)
    ktp_preview = ObjectProperty(None)
    kk_preview = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ktp_image = None
        self.kk_image = None
    
    def choose_ktp_image(self):
        popup = ImageChooserPopup(callback=self.on_ktp_image_selected)
        popup.open()

    def on_ktp_image_selected(self, file_path):
        self.ktp_image = file_path
        self.ktp_preview.source = file_path

    def choose_kk_image(self):
        popup = ImageChooserPopup(callback=self.on_kk_image_selected)
        popup.open()

    def on_kk_image_selected(self, file_path):
        self.kk_image = file_path
        self.kk_preview.source = file_path

    def clear_image(self):
        self.ktp_image = None
        self.kk_image = None
        self.ktp_preview.source = ''
        self.kk_preview.source = ''
    
    def add_spengantar(self):
        nama = self.name_input.text.strip()
        keperluan = self.keperluan_input.text.strip()
        
        if nama and keperluan:
            try:
                # Upload images if selected
                kk_image_url = None
                ktp_image_url = None
                
                if self.kk_image:
                    # Upload KK image
                    result_kk = StorageManager.upload_image(self.kk_image)
                    if result_kk["status"] == "success":
                        kk_image_url = result_kk["url"]
                
                if self.ktp_image:
                    # Upload KTP image
                    result_ktp = StorageManager.upload_image(self.ktp_image)
                    if result_ktp["status"] == "success":
                        ktp_image_url = result_ktp["url"]
                
                user_email = self.manager.user_email 

                # Create spengantar data
                spengantar_data = {
                    'nama': nama,
                    'keperluan': keperluan,
                    'kk_image_url': kk_image_url,
                    'ktp_image_url': ktp_image_url,
                    'user_email': user_email
                }
                
                Database.add_spengantar(spengantar_data)
                
                # Clear inputs
                self.name_input.text = ''
                self.keperluan_input.text = ''
                self.clear_image()  # Menghapus pratinjau gambar
                
                self.show_popup('Sukses', 'Pengajuan telah terkirim')
                self.manager.current = 'usurat'
            except ValueError:
                self.show_popup('Error', 'Keperluan dan stok harus berupa angka!')
            except Exception as e:
                self.show_popup('Error', f'Terjadi kesalahan: {str(e)}')
        else:
            self.show_popup('Error', 'Semua field harus diisi!')

    def show_popup(self, title, message):
        # Layout untuk menampilkan pesan popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))

        # Tombol untuk menutup popup
        close_button = Button(text="Tutup", size_hint=(1, 0.3))
        close_button.bind(on_press=lambda *args: popup.dismiss())
        content.add_widget(close_button)

        # Membuat popup dengan judul dan layout di atas
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
        popup.open()


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

    