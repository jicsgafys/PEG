from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from utils.widgets import AngelaStatusDialog, AngelaSingleTextInputDialog, \
    AngelaPopupFileManager, AngelaConfirmationDialog

from views.coords_adjustment.coords_adjustment_calculate_view import CoordsAdjustmentCalculateView

from models.coords_adjustment.coords_adjustment_model import CoordinatesAdjustment, save_csv_data


class CoordsAdjustmentCalculateController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget

        self.data = data

        self.ui = CoordsAdjustmentCalculateView()
        self.add_widget(self.ui)

        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()
        self.ui.action_buttons.next_button.on_release = lambda: self.perform_computations()

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
            del self
        except:
            pass

    def back_to_home_widget(self):
        self.back_to_previous_widget()
        self.previous_widget.back_to_previous_widget()
        del self

    def perform_computations(self):
        confirm_dialog = AngelaConfirmationDialog("", "Perform computations?")
        status_dialog = AngelaStatusDialog("Status", "")
        filename_dialog = AngelaSingleTextInputDialog("Output Filename", 'filename')
        folderpath_dialog = AngelaPopupFileManager('folder')

        confirm_dialog.yes_btn.on_release = lambda: continue_computations()
        confirm_dialog.no_btn.on_release = lambda: confirm_dialog.dialog.dismiss()
        confirm_dialog.dialog.open()

        def continue_computations():
            # {'filepath': self.data['filepath'],
            #  'column_match': column_match,
            #  'column_header': self.data['column_header'],
            #  'first_row_as_header': self.data['first_row_as_header']}
            weight_type = self.ui.weight_type_combo.drop_down_button.current_item
            confidence_level = self.ui.confidence_level_widget.drop_down_button.current_item

            confirm_dialog.dialog.dismiss()
            model = CoordinatesAdjustment(self.data['filepath'], self.data['first_row_as_header'],
                                          self.data['column_header'], self.data['matched_column_header'],
                                          weight_type, confidence_level)
            results = model.perform_computations()
            if results:
                status_dialog.dialog.text = "Successful!" \
                                            "\nContinue to save results?"
                status_dialog.dialog.buttons[-1].on_release = lambda: open_folderpath_dialog(results)
                status_dialog.dialog.open()


            else:
                status_dialog.dialog.dismiss()
                status_dialog.dialog.text = "Oops! Something went wrong" \
                                            "\nCheck your file data or matched columns and try again."
                status_dialog.dialog.buttons[-1].on_release = lambda: status_dialog.dialog.dismiss()
                status_dialog.dialog.open()

        def open_filename_dialog(data, folderpath):
            # status_dialog.dialog.dismiss()
            filename_dialog.dialog.buttons[-1].on_release = lambda: save_output(folderpath, data)
            filename_dialog.dialog.open()

        def open_folderpath_dialog(data):
            status_dialog.dialog.dismiss()  # Note

            folderpath_dialog.open_file_manager()

            folderpath_dialog.file_manager.select_path = \
                lambda x: open_filename_dialog(data, x)

        def back_to_home():
            self.back_to_home_widget()
            filename_dialog.dialog.dismiss()
            status_dialog.dialog.dismiss()
            folderpath_dialog.exit_manager()

            status_dialog.dialog.text = "Saved Successfully"
            status_dialog.dialog.buttons[-1].on_release = lambda: status_dialog.dialog.dismiss()
            status_dialog.dialog.open()
            # self.back_to_home_widget()

        def save_output(folderpath, data):
            filename = str(filename_dialog.dialog_content.first_entry.text).strip()
            filepath = str(folderpath) + "\\" + filename + ".csv"

            # folderpath_dialog.exit_manager()
            try:
                save_csv_data(filepath, data)
                back_to_home()

            except:
                status_dialog.dialog.text = "Failed! " \
                                            "\nCheck your filename"
                status_dialog.dialog.open()
                status_dialog.dialog.buttons[-1].on_release = lambda: status_dialog.dialog.dismiss()


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = CoordsAdjustmentCalculateController(None, None, None)

            return app


    MainApp().run()
