import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown

class Line(Widget):
    def __init__(self, **kwargs):
        super(Line, self).__init__(**kwargs)
        self.bind(size=self.update_line, pos=self.update_line)

    def update_line(self, *args):
        self.canvas.clear()  
        with self.canvas:
            kivy.graphics.Color(1, 1, 1, 1)  
            kivy.graphics.Rectangle(pos=self.pos, size=(self.width, 2))  

class MyApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=[0, 0, 0, 10])  

        # seting
        dropdown = DropDown()
        for option in ['Persuratan', 'Pengaduan', 'Logout']:
            btn = Button(text=option, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.handle_dropdown_select(btn.text))
            dropdown.add_widget(btn)
        log = Button(text='seting', size_hint=(0.2, 0.05), height=50)
        log.bind(on_release=dropdown.open)
        main_layout.add_widget(log)

        line = Line(size_hint_y=None, height=2)  
        main_layout.add_widget(line)

        label = Label(text="Selamat datang di desa Sanggang", size_hint_y=(0.2))
        main_layout.add_widget(label)

        line = Line(size_hint_y=None, height=2)  
        main_layout.add_widget(line)

        # pengumuman
        grid_layout = GridLayout(cols=4, size_hint=(1, 0.3), padding=[0, 0, 0, 10], spacing=2)  
        btn_grid1 = Button(text="pengumuman 1")
        btn_grid2 = Button(text="pengumuman 2")
        btn_grid3 = Button(text="pengumuman 3")
        btn_grid4 = Button(text="pengumuman 4")
        grid_layout.add_widget(btn_grid1)
        grid_layout.add_widget(btn_grid2)
        grid_layout.add_widget(btn_grid3)
        grid_layout.add_widget(btn_grid4)
        main_layout.add_widget(grid_layout)

        # berita
        playout = PageLayout(size_hint=(1, 0.3)) 
        btn1 = Button(text="berita 1", size_hint=(1, 1))
        btn2 = Button(text="berita 2", size_hint=(1, 1))
        btn3 = Button(text="berita 3", size_hint=(1, 1))
        playout.add_widget(btn1)
        playout.add_widget(btn2)
        playout.add_widget(btn3)
        main_layout.add_widget(playout)

        return main_layout

    def handle_dropdown_select(self, option):
        print(f'Pilihan dropdown: {option}') 

if __name__ == '__main__':
    MyApp().run()
