from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from utils.widgets import AngelaConfirmationDialog, AngelaStatusDialog, AngelaPopupFileManager, \
    AngelaSingleTextInputDialog
from views.geoid_model.geoid_prediction_model_column_matching_view \
    import GeoidModelPredictionColumnMatchingView

from models.geoid_model.geoid_model_model import ComputeGeoidModel, save_csv_data


class GeoidModelPredictionColumnMatchingController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        # A dictionary of the file path & bool of column headers as below
        # {'filepath': .csv, 'column_header': []}
        self.data = data

        self.ui = GeoidModelPredictionColumnMatchingView(self.data['predict_column_header'])
        self.add_widget(self.ui)

        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()
        self.ui.action_buttons.next_button.on_release = lambda: self.perform_computations()

    def get_prediction_column_matched(self):
        column_match = {"Station": str(self.ui.station_combo.drop_down_button.current_item),
                        "GPS Northing": str(self.ui.gps_northing_combo.drop_down_button.current_item),
                        "GPS Easting": str(self.ui.gps_easting_combo.drop_down_button.current_item),
                        "GPS Height": str(self.ui.gps_height_combo.drop_down_button.current_item)}
        self.data['predict_matched_column_header'] = column_match

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
            del self
        except:
            pass

    def back_to_home_widget(self):
        try:
            # self.back_to_previous_widget()
            # self.previous_widget.back_to_previous_widget()
            self.back_to_previous_widget()
            self.previous_widget.back_to_previous_widget()
            self.previous_widget.previous_widget.back_to_previous_widget()
        except:
            pass

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

            confirm_dialog.dialog.dismiss()
            self.get_prediction_column_matched()  # Note this one. Very vital
            model = ComputeGeoidModel(self.data['train_filepath'],
                                      self.data['train_first_row_as_header'],
                                      self.data['train_column_header'],
                                      self.data['train_matched_column_header'],
                                      self.data['predict_filepath'],
                                      self.data['predict_first_row_as_header'],
                                      self.data['predict_column_header'],
                                      self.data['predict_matched_column_header'])
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
            app = GeoidModelPredictionColumnMatchingView(["Column " + str(x) for x in range(10)])

            return app


    MainApp().run()
