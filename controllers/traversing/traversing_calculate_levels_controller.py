from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from views.traversing.traversing_calculate_levels_view import TraversingCalculateLevelsView


class TraversingCalculateLevelsController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget

        # This contains filepath, matched_columns in the format below
        # {'filepath': .csv, column_names:{'backsight': .., 'foresight': ...}}
        self.data = data

        self.ui = TraversingCalculateLevelsView()
        self.add_widget(self.ui)

        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
        except:
            pass

    def back_to_home_widget(self):
        pass


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = TraversingCalculateLevelsView()

            return app

    MainApp().run()