import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.login import LoginScreen
from screens.registrasi import RegistrasiScreen
from page.admin import AdminScreen
from page.user import UserScreen
from page.usurat import UsuratScreen
from page.upengaduan import UpengaduanScreen
from page.upengumuman import UpengumumanScreen
from page.ustruktur import Ustrukturscreen
from page.uproduk import UserProductList
from page.article import ProductList, AddProduct, EditProduct
from kivy.lang import Builder 
from kivy.core.window import Window
from page.apengumuman import PengumumanList, AddPengumuman, EditPengumuman
class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        Window.size = (360, 640)  # atur ukuran jendela ke 360x640
        kv_path = os.path.join(os.path.dirname(__file__), 'kivy')
        Builder.load_file(os.path.join(kv_path, 'login.kv'))
        Builder.load_file(os.path.join(kv_path, 'registrasi.kv'))
        Builder.load_file(os.path.join(kv_path, 'admin.kv'))
        Builder.load_file(os.path.join(kv_path, 'user.kv'))
        Builder.load_file(os.path.join(kv_path, 'usurat.kv'))
        Builder.load_file(os.path.join(kv_path, 'upengaduan.kv'))
        Builder.load_file(os.path.join(kv_path, 'article.kv'))
        Builder.load_file(os.path.join(kv_path, 'upengumuman.kv'))
        Builder.load_file(os.path.join(kv_path, 'ustruktur.kv'))
        Builder.load_file(os.path.join(kv_path, 'uproduk.kv'))
        Builder.load_file(os.path.join(kv_path, 'apengumuman.kv'))
        sm = MyScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistrasiScreen(name='registrasi'))
        sm.add_widget(AdminScreen(name='admin'))    
        sm.add_widget(UserScreen(name='user'))
        sm.add_widget(UsuratScreen(name='usurat'))
        sm.add_widget(UpengaduanScreen(name='upengaduan'))
        sm.add_widget(UpengumumanScreen(name='upengumuman'))
        sm.add_widget(Ustrukturscreen(name='ustruktur'))
        sm.add_widget(ProductList(name='product_list'))
        sm.add_widget(AddProduct(name='add_product'))
        sm.add_widget(EditProduct(name='edit_product'))
        sm.add_widget(UserProductList(name='uproduk'))
        sm.add_widget(PengumumanList(name='pengumuman_list'))
        sm.add_widget(AddPengumuman(name='add_pengumuman'))
        sm.add_widget(EditPengumuman(name='edit_pengumuman'))
        sm.current = 'login'  # Menetapkan layar yang ditampilkan pertama kali
        return sm

if __name__ == '__main__':
    MyApp().run()