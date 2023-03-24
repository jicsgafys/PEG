from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from views.beardist.beardist_column_matching_view import BearDistColumnMatchingView
from controllers.beardist.beardist_calculate_levels_controller import BearDistCalculateLevelsController


class BearDistColumnMatchingController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        # A dictionary of the file path & bool of column headers as below
        # {'filepath': .csv, 'column_header': []}
        self.data = data

        self.ui = BearDistColumnMatchingView(self.data['column_header'])
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
            column_match = {"Point": str(self.ui.point_combo.drop_down_button.current_item),
                            "Easting": str(self.ui.easting_combo.drop_down_button.current_item),
                            "Northing": str(self.ui.northing_combo.drop_down_button.current_item),
                            "Back Target": str(self.ui.backtarget_combo.drop_down_button.current_item),
                            "Station": str(self.ui.station_combo.drop_down_button.current_item),
                            "Fore Target": str(self.ui.foretarget_combo.drop_down_button.current_item)}

            beardist_calculate_levels_controller = \
                BearDistCalculateLevelsController(self.main_container_widget, self,
                                                  {'filepath': self.data['filepath'],
                                                   'matched_column_header': column_match,
                                                   'column_header': self.data['column_header'],
                                                   'first_row_as_header': self.data['first_row_as_header']})

            self.main_container_widget.remove_widget(self)
            self.clear_widgets()
            Clock.schedule_once(lambda x: transition(), 0)
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.main_container_widget.add_widget(beardist_calculate_levels_controller)
            beardist_calculate_levels_controller.size_hint_y = 0
            anim.start(beardist_calculate_levels_controller)


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = BearDistColumnMatchingController(
                None, None, {'filepath': None, 'column_header': [f'Col {x + 1}' for x in range(5)]})

            return app


    MainApp().run()
