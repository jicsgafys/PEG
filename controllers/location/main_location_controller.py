from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from controllers.location.location_map_controller import LocationMapController


class MainLocationController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        # Default home screen for the page
        self.location_map_controller = LocationMapController()
        self.add_widget(self.location_map_controller)

        # Bindings


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = MainLocationController()

            return app


    MainApp().run()
