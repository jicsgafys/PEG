from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from controllers.levelling.levelling_file_upload_controller import LevellingFileUploadController
from controllers.levelling.levelling_column_matching_controller import LevellingColumnMatchingController
from models.levelling.levelling_model import ColumnHeader


class MainLevellingController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        # Default home screen for the page
        self.levelling_file_upload_controller = LevellingFileUploadController()
        self.add_widget(self.levelling_file_upload_controller)

        # Instantiate the other widget
        # self.levelling_column_matching_controller = LevellingColumnMatchingController(
        #     self, self.levelling_file_upload_controller, {'filepath': None, 'column_header': ()})

        # Bindings
        self.levelling_file_upload_controller.ui.action_buttons.next_button.on_release = \
            lambda: self.show_column_matching()

    def show_column_matching(self):
        try:
            # Note how this implementation is done
            file_path = self.levelling_file_upload_controller.ui.file_upload.upload_input_entry.text
            first_row_is_header = self.levelling_file_upload_controller.ui.header_checkbutton.checkbox.active
            csv_header = self.get_csv_file_header()

            if csv_header:
                levelling_column_matching_controller = LevellingColumnMatchingController(
                    self, self.levelling_file_upload_controller,
                    {'filepath': file_path, 'column_header': csv_header,
                     'first_row_as_header': first_row_is_header})

                self.remove_widget(self.levelling_file_upload_controller)
                self.clear_widgets()
                Clock.schedule_once(lambda x: transition(), 0)
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.add_widget(levelling_column_matching_controller)
            levelling_column_matching_controller.size_hint_y = 0
            anim.start(levelling_column_matching_controller)

    def get_csv_file_header(self):
        file_path = self.levelling_file_upload_controller.ui.file_upload.upload_input_entry.text
        first_row_is_header = self.levelling_file_upload_controller.ui.header_checkbutton.checkbox.active
        if file_path:
            model = ColumnHeader(file_path, first_row_is_header)
            header = model.get_column_header()

            return header


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = MainLevellingController()

            return app


    MainApp().run()
