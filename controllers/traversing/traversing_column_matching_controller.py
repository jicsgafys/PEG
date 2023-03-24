from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from views.traversing.traversing_column_matching_view import TraversingColumnMatchingView
from controllers.traversing.traversing_calculate_levels_controller import TraversingCalculateLevelsController


class TraversingColumnMatchingController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, data):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        # A dictionary of the file path & bool of column headers as below
        # {'filepath': .csv, 'column_header': []}
        self.data = data

        self.ui = TraversingColumnMatchingView(self.data['column_header'])
        self.add_widget(self.ui)

        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()
        self.ui.action_buttons.next_button.on_release = lambda: self.move_to_next_widget()

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
        except:
            pass

    def move_to_next_widget(self):
        try:
            traversing_calculate_levels_controller = \
                TraversingCalculateLevelsController(self.main_container_widget, self,
                                                    {'filepath': None, 'column_names': {}})
            self.main_container_widget.remove_widget(self)

            Clock.schedule_once(lambda x: transition(), 0)
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.main_container_widget.add_widget(traversing_calculate_levels_controller)
            traversing_calculate_levels_controller.size_hint_y = 0
            anim.start(traversing_calculate_levels_controller)


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = TraversingColumnMatchingController(
                None, None, {'filepath': None, 'column_header': [f'Col {x + 1}' for x in range(5)]})

            return app


    MainApp().run()
