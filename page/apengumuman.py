import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from database import FirebaseDB
from tenacity import retry, stop_after_attempt, wait_fixed # Sesuaikan dengan implementasi database Anda

class Pengumuman(FirebaseDB):

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get_all_pengumumans():
        try:
            pengumumans = FirebaseDB.db.child("pengumumans").get()
            if pengumumans.each():
                return [(pengumuman.key(), pengumuman.val()) for pengumuman in pengumumans.each()]
            return []
        except Exception as e:
            print(f"Error getting pengumumans: {e}")
            return []

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def add_pengumuman(pengumuman_data):
        try:
            return FirebaseDB.db.child("pengumumans").push(pengumuman_data)
        except Exception as e:
            print(f"Error adding pengumuman: {e}")
            raise e

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def update_pengumuman(pengumuman_id, pengumuman_data):
        try:
            return FirebaseDB.db.child("pengumumans").child(pengumuman_id).update(pengumuman_data)
        except Exception as e:
            print(f"Error updating pengumuman: {e}")
            raise e

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def delete_pengumuman(pengumuman_id):
        try:
            return FirebaseDB.db.child("pengumumans").child(pengumuman_id).remove()
        except Exception as e:
            print(f"Error deleting pengumuman: {e}")
            raise e

# Kelas untuk item pengumuman
# Modifikasi di kelas PengumumanItem untuk tampilan label yang lebih rapi
class PengumumanItem(BoxLayout):
    def __init__(self, pengumuman_id, pengumuman_data, edit_callback, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # Ubah orientasi menjadi vertikal
        self.size_hint_y = None
        self.height = 200  # Tambah tinggi untuk ruang label dan tombol
        self.padding = 10
        self.spacing = 2

        with self.canvas.before:
            Color(0, 0, 0, 0.19)
            self.shadow_rect1 = RoundedRectangle(pos=self.pos, size=self.size, radius=[5])
            Color(0, 0, 0, 0.19)
            self.shadow_rect2 = RoundedRectangle(pos=self.pos, size=self.size, radius=[5])
            Color(0, 0, 0, 0.23)
            self.shadow_rect3 = RoundedRectangle(pos=self.pos, size=(self.width, self.height + 5), radius=[5])

        with self.canvas:
            Color(1, 1, 1, 1)  # Warna latar belakang
            self.background_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5])   

        # Bind ukuran agar otomatis update shadow
        self.bind(pos=self.update_canvas, size=self.update_canvas)

        # Menampilkan data pengumuman
        label_text = (
            f"[color=#000000][b]Judul:[/b] {pengumuman_data.get('judul', 'No Title')}\n"
        )

        self.label = Label(
            text=label_text, halign='left', valign='center',
            text_size=(self.width, None), markup=True
        )
        self.label.bind(size=self._update_text_size)  # Bind untuk memperbarui ukuran teks
        self.add_widget(self.label)

        # Layout horizontal untuk tombol edit dan hapus
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35, spacing=2)
        self.edit_button = Button(text='Edit', size_hint=(0.5, 1))
        self.edit_button.bind(on_press=lambda x: edit_callback(pengumuman_id, pengumuman_data))
        button_layout.add_widget(self.edit_button)

        self.delete_button = Button(text='Hapus', size_hint=(0.5, 1))
        self.delete_button.bind(on_press=lambda x: delete_callback(pengumuman_id))
        button_layout.add_widget(self.delete_button)

        # Tambahkan layout tombol ke dalam item
        self.add_widget(button_layout)

    def _update_text_size(self, *args):
        self.label.text_size = (self.label.width, None)

    def update_canvas(self, *args):
        # Update posisi dan ukuran shadow dan background saat ukuran item berubah
        self.shadow_rect1.pos = (self.x - 2, self.y)
        self.shadow_rect1.size = self.size
        self.shadow_rect2.pos = (self.x + 2, self.y)
        self.shadow_rect2.size = self.size
        self.shadow_rect3.pos = (self.x, self.y - 4)
        self.shadow_rect3.size = (self.width, self.height + 5)

         # Update posisi dan ukuran background
        self.background_rect.pos = self.pos
        self.background_rect.size = self.size


# Kelas untuk daftar pengumuman
class PengumumanList(Screen):
    container = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        if self.container is None:
            print("Container belum terhubung!")
        else:
            print("Container terhubung dengan sukses.")

    def on_enter(self):
        self.load_pengumumans()

    def load_pengumumans(self):
        print("Memuat pengumuman...")
        if not self.container:
            print("Container tidak ditemukan!")
            return

        self.container.clear_widgets()  # Kosongkan kontainer

        # Dapatkan data pengumuman
        pengumumans = Pengumuman.get_all_pengumumans()
        print("Data yang diambil:", pengumumans)

        if pengumumans:
            for pengumuman_id, pengumuman_data in pengumumans:
                print(f"Menambahkan pengumuman: {pengumuman_id} - {pengumuman_data}")
                pengumuman_item = PengumumanItem(
                    pengumuman_id,
                    pengumuman_data,
                    self.edit_pengumuman,
                    self.delete_pengumuman
                )
                self.container.add_widget(pengumuman_item)
                self.container.add_widget(Label(size_hint_y=None, height=10))
        else:
            print("Tidak ada pengumuman ditemukan.")
            self.container.add_widget(Label(text="Tidak ada pengumuman tersedia"))


    def show_add_pengumuman(self):
        self.manager.current = 'add_pengumuman'

    def edit_pengumuman(self, pengumuman_id, pengumuman_data):
        edit_screen = self.manager.get_screen('edit_pengumuman')
        edit_screen.set_pengumuman(pengumuman_id, pengumuman_data)
        self.manager.current = 'edit_pengumuman'

    def delete_pengumuman(self, pengumuman_id):
        confirm_popup = Popup(
            title='Konfirmasi Hapus',
            content=BoxLayout(orientation='vertical', padding=10, spacing=10),
            size_hint=(None, None),
            size=(300, 200)
        )

        # Pesan konfirmasi
        confirm_popup.content.add_widget(Label(text='Apakah Anda yakin ingin menghapus pengumuman ini?', halign="center"))

        # Tombol konfirmasi
        confirm_button = Button(text='Ya', size_hint=(1, 0.3))
        confirm_button.bind(on_release=lambda x: self.confirm_delete(pengumuman_id, confirm_popup))
        confirm_popup.content.add_widget(confirm_button)

        # Tombol batal
        cancel_button = Button(text='Tidak', size_hint=(1, 0.3))
        cancel_button.bind(on_release=confirm_popup.dismiss)
        confirm_popup.content.add_widget(cancel_button)

        confirm_popup.open()

    def confirm_delete(self, pengumuman_id, confirm_popup):
        Pengumuman.delete_pengumuman(pengumuman_id)
        self.load_pengumumans()
        confirm_popup.dismiss()



# Kelas untuk menambahkan pengumuman
class AddPengumuman(Screen):
    judul_input = ObjectProperty(None)
    # tanggal_input = ObjectProperty(None)
    isi_input = ObjectProperty(None)
    waktu_input = ObjectProperty(None)
    tempat_input = ObjectProperty(None)
    pengingat_tambahan_input = ObjectProperty(None)

    def add_pengumuman(self):
        pengumuman_data = {
            'judul': self.ids.judul_input.text.strip() ,
            # 'tanggal': self.ids.tanggal_input.text.strip(),
            'isi': self.ids.isi_input.text.strip(),
            'waktu': self.ids.waktu_input.text.strip(),
            'tempat': self.ids.tempat_input.text.strip(),
            'pengingat_tambahan': self.ids.pengingat_tambahan_input.text.strip(),
        }
        if pengumuman_data['judul'] and pengumuman_data['isi'] and pengumuman_data['waktu']:
            Pengumuman.add_pengumuman(pengumuman_data)
            self.manager.current = 'pengumuman_list'
        else:
            popup = Popup(title='Error', content=Label(text='Field Judul, isi, dan waktu tidak boleh kosong'), size_hint=(None, None), size=(400, 200))
            popup.open()

# Kelas untuk mengedit pengumuman
class EditPengumuman(Screen):
    pengumuman_id = StringProperty(None)
    judul_input = ObjectProperty(None)
    # tanggal_input = ObjectProperty(None)
    isi_input = ObjectProperty(None)
    waktu_input = ObjectProperty(None)
    tempat_input = ObjectProperty(None)
    pengingat_tambahan_input = ObjectProperty(None)

    def set_pengumuman(self, pengumuman_id, pengumuman_data):
        self.pengumuman_id = pengumuman_id
        self.judul_input = self.ids.judul_input
        # self.tanggal_input = self.ids.tanggal_input
        self.isi_input = self.ids.isi_input
        self.waktu_input = self.ids.waktu_input
        self.tempat_input = self.ids.tempat_input
        self.pengingat_tambahan_input = self.ids.pengingat_tambahan_input
        
        self.judul_input.text = pengumuman_data.get('judul', '')
        # self.tanggal_input.text = pengumuman_data.get('tanggal', '')
        self.isi_input.text = pengumuman_data.get('isi', '')
        self.waktu_input.text = pengumuman_data.get('waktu', '')
        self.tempat_input.text = pengumuman_data.get('tempat', '')
        self.pengingat_tambahan_input.text = pengumuman_data.get('pengingat_tambahan', '')

    def update_pengumuman(self):
        updated_data = {
            'judul': self.ids.judul_input.text.strip(),
            # 'tanggal': self.ids.tanggal_input.text.strip(),
            'isi': self.ids.isi_input.text.strip(),
            'waktu': self.ids.waktu_input.text.strip(),
            'tempat': self.ids.tempat_input.text.strip(),
            'pengingat_tambahan': self.ids.pengingat_tambahan_input.text.strip(),
        }
        if updated_data['judul'] and updated_data['isi'] and updated_data['waktu']:
            Pengumuman.update_pengumuman(self.pengumuman_id, updated_data)
            self.manager.current = 'pengumuman_list'
        else:
            popup = Popup(title='Error', content=Label(text='Field Judul, isi, dan waktu tidak boleh kosong'), size_hint=(None, None), size=(400, 200))
            popup.open()