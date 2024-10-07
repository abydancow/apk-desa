from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class AdminWidget(BoxLayout):
    pass

class AdminApp(App):
    def build(self):
        return AdminWidget()

if __name__ == '__main__':
    AdminApp().run()

