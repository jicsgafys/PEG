from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from views.about_us.about_us_view import AboutUsView


class AboutUsController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        self.ui = AboutUsView()
        self.add_widget(self.ui)


if __name__ == "__main__":
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()
            self.title = "Angela"
            # self.icon = str(ICONS_FOLDER_PATH).replace('\\', '/') + 'app_icon.ico'
            # print(self.icon)

        def build(self):
            # return MDBoxLayout()
            homeview = AboutUsController()
            return homeview

    MainApp().run()