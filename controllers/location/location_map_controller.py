from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from views.location.location_map_view import LocationMapView


class LocationMapController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        self.ui = LocationMapView()
        self.add_widget(self.ui)


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = LocationMapController()

            return app

    MainApp().run()