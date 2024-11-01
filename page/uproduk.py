# user.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from database import FirebaseDB
from tenacity import retry, stop_after_attempt, wait_fixed

class Database(FirebaseDB):

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get_all_products():
        try:
            products = FirebaseDB.db.child("products").get()
            if products.each():
                return [(product.key(), product.val()) for product in products.each()]
            return []
        except Exception as e:
            print(f"Error getting products: {e}")
            return []

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def add_product(product_data):
        try:
            return FirebaseDB.db.child("products").push(product_data)
        except Exception as e:
            print(f"Error adding product: {e}")
            raise e

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def update_product(product_id, product_data):
        try:
            return FirebaseDB.db.child("products").child(product_id).update(product_data)
        except Exception as e:
            print(f"Error updating product: {e}")
            raise e

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def delete_product(product_id):
        try:
            return FirebaseDB.db.child("products").child(product_id).remove()
        except Exception as e:
            print(f"Error deleting product: {e}")
            raise e

class UserProductList(Screen):
    container = ObjectProperty(None)

    def on_enter(self):
        self.load_products()

    def load_products(self):
        self.container.clear_widgets()
        products = Database.get_all_products()

        if products:
            for product_id, product_data in products:
                product_item = ProductItem(
                    product_id,
                    product_data
                )
                self.container.add_widget(product_item)
        else:
            self.container.add_widget(
                Label(
                    text="Tidak ada produk tersedia",
                    size_hint_y=None,
                    height=100
                )
            )

class ProductItem(BoxLayout):
    def __init__(self, product_id, product_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 150
        self.padding = 5
        self.spacing = 10

        self.product_id = product_id
        self.product_data = product_data

        # Create image layout
        image_layout = BoxLayout(size_hint_x=0.3, padding=5)
        image_url = product_data.get('image_url', None)
        if image_url:
            product_image = AsyncImage(
                source=image_url,
                allow_stretch=True,
                keep_ratio=True
            )
            image_layout.add_widget(product_image)
        else:
            image_layout.add_widget(
                Label(
                    text='No Image',
                    color=(0.5, 0.5, 0.5, 1)
                )
            )

        # Create info layout
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)

        name = product_data.get('nama', 'No Name')
        price = product_data.get('harga', 0)
        stock = product_data.get('stok', 0)

        info_label = Label(
            text=f"Nama: {name}\nHarga: Rp {price:,.0f}\nStok: {stock}",
            size_hint_y=None,
            height=100,
            halign='left',
            valign='middle'
        )
        info_label.bind(size=info_label.setter('text_size'))
        info_layout.add_widget(info_label)

        self.add_widget(image_layout)
        self.add_widget(info_layout)
