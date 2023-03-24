from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock

from views.levelling.levelling_column_matching_view import LevellingColumnMatchingView
from controllers.levelling.levelling_calculate_levels_controller import LevellingCalculateLevelsController


class LevellingColumnMatchingController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        # A dictionary of the file path & bool of column headers as below
        # {'filepath': .csv, 'column_header': []}
        self.data = data

        self.ui = LevellingColumnMatchingView(self.data['column_header'])
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
            column_match = {"BS": str(self.ui.backsight_combo.drop_down_button.current_item),
                            "IS": str(self.ui.intersight_combo.drop_down_button.current_item),
                            "FS": str(self.ui.foresight_combo.drop_down_button.current_item),
                            "Remark": str(self.ui.remark_combo.drop_down_button.current_item)}
            levelling_calculate_levels_controller = LevellingCalculateLevelsController(
                self.main_container_widget, self, {'filepath': self.data['filepath'],
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
            self.main_container_widget.add_widget(levelling_calculate_levels_controller)
            levelling_calculate_levels_controller.size_hint_y = 0
            anim.start(levelling_calculate_levels_controller)


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = LevellingColumnMatchingController(
                None, None, {'filepath': None, 'column_header': [f'Col {x + 1}' for x in range(5)]})

            return app

    MainApp().run()