from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from models.geoid_model.geoid_model_model import ColumnHeader
from utils.paths import DISK_ROOT_PATH
from views.geoid_model.geoid_model_prediction_file_upload_view import \
    GeoidModelPredictionFileUploadView

from controllers.geoid_model.geoid_prediction_model_column_matching_controller import \
    GeoidModelPredictionColumnMatchingController


class GeoidModelPredictionFileUploadController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        self.data = data

        self.ui = GeoidModelPredictionFileUploadView()
        self.add_widget(self.ui)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            selector='file',
            ext=['.csv', ]
        )

        self.ui.file_upload.upload_button.on_release = lambda: self.open_file_manager()
        self.ui.file_upload.clear_button.on_release = lambda: self.clear_upload_entry()
        self.ui.action_buttons.back_button.on_release = \
            lambda: self.back_to_previous_widget()
        self.ui.action_buttons.next_button.on_release = \
            lambda: self.move_to_next_widget()

    def open_file_manager(self):
        self.file_manager.show(DISK_ROOT_PATH)

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.exit_manager()
        self.ui.file_upload.upload_input_entry.readonly = False
        self.ui.file_upload.upload_input_entry.set_text(self, "")
        self.ui.file_upload.upload_input_entry.set_text(self, str(path))
        self.ui.file_upload.upload_input_entry.readonly = True

    def clear_upload_entry(self):
        self.ui.file_upload.upload_input_entry.readonly = False
        self.ui.file_upload.upload_input_entry.set_text(self, "")
        self.ui.file_upload.upload_input_entry.readonly = True

    def move_to_next_widget(self):
        file_path = self.ui.file_upload.upload_input_entry.text
        first_row_is_header = self.ui.header_checkbutton.checkbox.active
        csv_header = self.get_csv_file_header()
        try:
            adjustment_calculate_controller = GeoidModelPredictionColumnMatchingController(
                self.main_container_widget, self,
                {'train_filepath': self.data['train_filepath'],
                 'train_matched_column_header': self.data['train_matched_column_header'],
                 'train_column_header': self.data['train_column_header'],
                 'train_first_row_as_header': self.data['train_first_row_as_header'],
                 'predict_filepath': file_path, 'predict_first_row_as_header': first_row_is_header,
                 'predict_column_header': csv_header})
            self.main_container_widget.remove_widget(self)
            self.clear_widgets()
            Clock.schedule_once(lambda x: transition(), 0)  # Note; Just for anime
        except Exception as e:
            print(e)
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.main_container_widget.add_widget(adjustment_calculate_controller)
            adjustment_calculate_controller.size_hint_y = 0
            anim.start(adjustment_calculate_controller)

    def get_csv_file_header(self):
        file_path = self.ui.file_upload.upload_input_entry.text
        first_row_is_header = self.ui.header_checkbutton.checkbox.active
        if file_path:
            model = ColumnHeader(file_path, first_row_is_header)
            header = model.get_column_header()

            return header

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
            del self

        except:
            pass


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = GeoidModelPredictionFileUploadController(None, None, None)

            return app

    MainApp().run()