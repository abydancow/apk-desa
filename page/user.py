import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout


Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False) 


class MyGrid(Widget):
    pass


class UserApp(App):
    def build(self):
        kv_file_path = os.path.join(os.path.dirname(__file__), '..', 'kivy', 'user.kv')
        Builder.load_file(kv_file_path)
        return MyGrid()
    
if __name__ =="__main__":
    UserApp() .run()