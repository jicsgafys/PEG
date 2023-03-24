from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from controllers.traversing.traversing_file_upload_controller import TraversingFileUploadController
from controllers.traversing.traversing_column_matching_controller import TraversingColumnMatchingController


class MainTraversingController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        # Default home screen for the page
        self.traversing_file_upload_controller = TraversingFileUploadController()
        self.add_widget(self.traversing_file_upload_controller)

        # Bindings
        self.traversing_file_upload_controller.ui.action_buttons.next_button.on_release = \
            lambda: self.show_column_matching()

    def show_column_matching(self):
        try:
            traversing_column_matching_controller = TraversingColumnMatchingController(
                self, self.traversing_file_upload_controller, {'filepath': None, 'column_header': ()})
            Clock.schedule_once(lambda x: transition(), 0)
            self.remove_widget(self.traversing_file_upload_controller)

        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.add_widget(traversing_column_matching_controller)
            traversing_column_matching_controller.size_hint_y = 0
            anim.start(traversing_column_matching_controller)


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = MainTraversingController()

            return app


    MainApp().run()
