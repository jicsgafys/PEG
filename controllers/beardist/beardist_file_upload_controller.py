from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from utils.paths import DISK_ROOT_PATH
from views.beardist.beardist_file_upload_view import BearDistFileUploadView


class BearDistFileUploadController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        self.ui = BearDistFileUploadView()
        self.add_widget(self.ui)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            selector='file',
            ext=['.csv', ]
        )

        self.ui.file_upload.upload_button.on_release = lambda: self.open_file_manager()
        self.ui.file_upload.clear_button.on_release = lambda: self.clear_upload_entry()

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


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = BearDistFileUploadController()

            return app

    MainApp().run()