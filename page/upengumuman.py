from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from tenacity import retry, stop_after_attempt, wait_fixed
from database import FirebaseDB
from kivy.graphics import Line



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

class PengumumanItem(BoxLayout):
    def __init__(self, pengumuman_id, pengumuman_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 650
        self.width = 450
        self.padding = 30
        # self.spacing = 5

        # Mengatur tampilan latar belakang dengan shadow
        with self.canvas.before:
            Color(0, 0, 0, 0.19)
            self.shadow_rect1 = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            Color(0, 0, 0, 0.19)
            self.shadow_rect2 = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            Color(0, 0, 0, 0.23)
            self.shadow_rect3 = RoundedRectangle(pos=self.pos, size=(self.width, self.height + 5), radius=[20])

        with self.canvas:
            Color(1, 1, 1, 1)  # Warna latar belakang
            self.background_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])   

        # Bind ukuran agar otomatis update shadow
        self.bind(pos=self.update_canvas, size=self.update_canvas)

        # Label untuk menampilkan pengumuman
        self.add_widget(Label(
            text=f"[/b] {pengumuman_data.get('judul', 'No Title')}",
            # size_hint_y=None,
            # height=60,
            markup=True,
            color=(0, 0, 0, 1),
            size_hint_y=0.15,
            # text_size=(self.width - 200, None),
            # halign='center' 
        ))
        with self.canvas.after:
            Color(0, 0, 0, 1)  # Warna garis hitam
            self.judul_line = Line(
                points=[self.x + 20, self.y + self.height - 100, self.x + self.width - 20, self.y + self.height - 100],
                width=1
            )
        
        
        self.add_widget(Label(
            text=f"[b]Isi:[/b] {pengumuman_data.get('isi', 'No Content')}",
            size_hint_y=0.5,  # Mengambil 50% dari tinggi total
            pos_hint={'x': 0.05, 'top': 0.9},  # Atur posisi horizontal dan tinggi label
            markup=True,
            text_size=(self.width - 40, None),  # Membatasi lebar teks agar terbungkus
            valign="top",  # Mengatur teks agar rata atas
            halign="left",  # Mengatur teks agar rata kiri
            color=(0, 0, 0, 1), # Atur posisi x dan center_y
        ))

        self.add_widget(Label(
            text=f"[b]Waktu:[/b] {pengumuman_data.get('waktu', 'No Time')}",
            # size_hint_y=None,
            # height=50,
            markup=True,
            text_size=(self.width - 40, None),
            # halign="left",
            color=(0, 0, 1, 1),
            size_hint_y=0.1,  # Atur posisi x dan center_y
        ))

        self.add_widget(Label(
            text=f"[b]Tempat:[/b] {pengumuman_data.get('tempat', 'No PIC')}",
            # size_hint_y=None,
            # height=50,
            markup=True,
            text_size=(self.width - 40, None),
            # halign="left",
            color=(0.8, 0.5, 0, 1),
            size_hint_y=0.1, # Atur posisi x dan center_y
        ))

        with self.canvas.after:
            Color(0, 0, 0, 1)  # Warna garis hitam
            self.judul_line = Line(
                points=[self.x + 20, self.y + self.height - 550, self.x + self.width - 20, self.y + self.height - 550],
                width=1
            )

        self.add_widget(Label(
            text=f"[b]NB:[/b] {pengumuman_data.get('pengingat_tambahan', 'No Reminder')}",
            # size_hint_y=None,
            # height=50,
            markup=True,
            text_size=(self.width - 40, None),
            halign="left",
            color=(0, 0, 0, 1),
            size_hint_y=0.1,  # Atur posisi x dan center_y
        ))

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


class UpengumumanScreen(Screen):
    container = ObjectProperty(None)

    def on_enter(self):
        self.load_pengumumans()

    def load_pengumumans(self):
        self.container.clear_widgets()  # Pastikan container kosong
        print("Loading pengumumans...")  # Debug: memastikan fungsi dijalankan

        pengumumans = Pengumuman.get_all_pengumumans()
        
        if not pengumumans:
            print("Tidak ada data pengumuman yang ditemukan.")
            self.container.add_widget(Label(text="Tidak ada pengumuman tersedia"))
        else:
            total_width = 0  # Inisialisasi total lebar
            
            for pengumuman_id, pengumuman_data in pengumumans:
                print(f"Menambahkan pengumuman ID: {pengumuman_id}, Data: {pengumuman_data}")  # Debug
                pengumuman_item = PengumumanItem(pengumuman_id, pengumuman_data)
                
                total_width += pengumuman_item.width  # Tambahkan lebar item pengumuman
                self.container.add_widget(pengumuman_item)

            self.container.size_hint_x = None  # Nonaktifkan size_hint_x
            self.container.width = total_width  # Atur lebar container sesuai total lebar pengumuman

 
