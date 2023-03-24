from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout


from views.home.home_view import HomeView


class HomeController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        self.ui = HomeView()
        self.add_widget(self.ui)


if __name__ == "__main__":
    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            home_controller = HomeController()
            return home_controller


    MainApp().run()