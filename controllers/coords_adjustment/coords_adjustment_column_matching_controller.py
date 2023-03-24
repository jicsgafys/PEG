from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from views.coords_adjustment.coords_adjustment_column_matching_view import \
    CoordsAdjustmentColumnMatchingView
from controllers.coords_adjustment.coords_adjustment_calculate_controller import \
    CoordsAdjustmentCalculateController


class CoordsAdjustmentColumnMatchingController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        # A dictionary of the file path & bool of column headers as below
        # {'filepath': .csv, 'column_header': []}
        self.data = data

        self.ui = CoordsAdjustmentColumnMatchingView(self.data['column_header'])
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
                            "Control": str(self.ui.control_combo.drop_down_button.current_item),
                            "Easting": str(self.ui.easting_combo.drop_down_button.current_item),
                            "Northing": str(self.ui.northing_combo.drop_down_button.current_item),
                            "Height": str(self.ui.height_combo.drop_down_button.current_item),
                            "From": str(self.ui.from_combo.drop_down_button.current_item),
                            "To": str(self.ui.to_combo.drop_down_button.current_item),
                            "Change_easting": str(self.ui.change_easting_combo.drop_down_button.current_item),
                            "Change_northing": str(self.ui.change_northing_combo.drop_down_button.current_item),
                            "Change_height": str(self.ui.change_height_combo.drop_down_button.current_item),
                            "Weight": str(self.ui.weight_combo.drop_down_button.current_item)}
            adjustment_calculate_controller = CoordsAdjustmentCalculateController(
                self.main_container_widget, self, {'filepath': self.data['filepath'],
                                                   'matched_column_header': column_match,
                                                   'column_header': self.data['column_header'],
                                                   'first_row_as_header': self.data['first_row_as_header']})
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
            app = CoordsAdjustmentColumnMatchingController(
                None, None, {'filepath': None, 'column_header': [f'Col {x + 1}' for x in range(5)]})

            return app

    MainApp().run()