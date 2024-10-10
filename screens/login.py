import os
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
# from kivy.graphics import Color, Line, Rectangle 
from kivy.config import Config
from kivy.lang import Builder 
from kivy.uix.widget import Widget
from kivy.core.window import Window


class Login(FloatLayout):
    pass

class LoginApp(App):
    def build(self):
        Window.size = (360, 640)  
        kv_file_path = os.path.join(os.path.dirname(__file__), '..', 'kivy', 'login.kv')
        Builder.load_file(kv_file_path)
        return Login()

if __name__ =="__main__":
    LoginApp().run()