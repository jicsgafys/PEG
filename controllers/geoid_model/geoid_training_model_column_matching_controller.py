from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from views.geoid_model.geoid_training_model_column_matching_view import \
    GeoidModelTrainingColumnMatchingView

from controllers.geoid_model.geoid_model_prediction_file_upload_controller \
    import GeoidModelPredictionFileUploadController


class GeoidModelTrainingColumnMatchingController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        # A dictionary of the file path & bool of column headers as below
        # {'filepath': .csv, 'column_header': []}
        self.data = data

        self.ui = GeoidModelTrainingColumnMatchingView(self.data['train_column_header'])
        self.add_widget(self.ui)

        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()
        self.ui.action_buttons.next_button.on_release = lambda: self.move_to_next_widget()

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
            del self
        except:
            pass

    def move_to_next_widget(self):
        try:
            column_match = {"Station": str(self.ui.station_combo.drop_down_button.current_item),
                            "Base Station": str(self.ui.base_station_combo.drop_down_button.current_item),
                            "GPS Northing": str(self.ui.gps_northing_combo.drop_down_button.current_item),
                            "GPS Easting": str(self.ui.gps_easting_combo.drop_down_button.current_item),
                            "GPS Height": str(self.ui.gps_height_combo.drop_down_button.current_item),
                            "Orthometric Height":
                                str(self.ui.orthometric_height_combo.drop_down_button.current_item)}
            adjustment_calculate_controller = GeoidModelPredictionFileUploadController(
                self.main_container_widget, self,
                {'train_filepath': self.data['train_filepath'],
                 'train_matched_column_header': column_match,
                 'train_column_header': self.data['train_column_header'],
                 'train_first_row_as_header': self.data['train_first_row_as_header']})
            self.main_container_widget.remove_widget(self)
            self.clear_widgets()
            Clock.schedule_once(lambda x: transition(), 0)  # Note; Just for anime
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.main_container_widget.add_widget(adjustment_calculate_controller)
            adjustment_calculate_controller.size_hint_y = 0
            anim.start(adjustment_calculate_controller)


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = GeoidModelTrainingColumnMatchingController(None, None, None)

            return app


    MainApp().run()
