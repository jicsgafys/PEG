from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from controllers.home.home_controller import HomeController
from controllers.levelling.main_levelling_controller import MainLevellingController
from controllers.location.main_location_controller import MainLocationController
from controllers.traversing.main_traversing_controller import MainTraversingController
from controllers.beardist.main_beardist_controller import MainBearDistController
from controllers.notes.main_note_controller import MainNoteController
from controllers.todos.main_todo_controller import MainTodoController
from controllers.about_us.about_us_controller import AboutUsController
from controllers.levels_adjustment.main_levels_adjustment_controller import MainAdjustmentController
from controllers.coords_adjustment.main_coords_adjustment_controller import MainCoordsAdjustmentController
from controllers.geoid_model.main_geoid_model_controller import MainGeoidModelController


class MainHomeController(MDBoxLayout):
    def __init__(self):
        super().__init__()
        # Set the homepage first
        self.home_controller = HomeController()
        self.add_widget(self.home_controller)

        # Commands to various pages using the side navigation menu
        self.home_controller.ui.levelling_nav_button.on_release = \
            lambda: self.show_levelling_page()
        self.home_controller.ui.traversing_nav_button.on_release = \
            lambda: self.show_traversing_page()
        self.home_controller.ui.beardist_nav_button.on_release = \
            lambda: self.show_beardist_page()
        self.home_controller.ui.todo_nav_button.on_release = \
            lambda: self.show_todo_page()
        self.home_controller.ui.note_nav_button.on_release = \
            lambda: self.show_note_page()
        self.home_controller.ui.about_nav_button.on_release = \
            lambda: self.show_about_us_page()
        self.home_controller.ui.levels_adjustment_nav_button.on_release = \
            lambda: self.show_levels_adjustment_page()
        self.home_controller.ui.coords_adjustment_nav_button.on_release = \
            lambda: self.show_coords_adjustment_page()
        self.home_controller.ui.geoid_model_nav_button.on_release = \
            lambda: self.show_geoid_model_page()
        self.home_controller.ui.location_nav_button.on_release = \
            lambda: self.show_location_page()

        # Commands to various pages using the homepage buttons
        self.home_controller.ui.home_levelling_button.on_release = \
            lambda: self.show_levelling_page()
        self.home_controller.ui.home_traversing_button.on_release = \
            lambda: self.show_traversing_page()
        self.home_controller.ui.home_beardist_button.on_release = \
            lambda: self.show_beardist_page()
        self.home_controller.ui.home_todo_button.on_release = \
            lambda: self.show_todo_page()
        self.home_controller.ui.home_note_button.on_release = \
            lambda: self.show_note_page()
        self.home_controller.ui.home_about_button.on_release = \
            lambda: self.show_about_us_page()
        self.home_controller.ui.home_levels_adjustment_button.on_release = \
            lambda: self.show_levels_adjustment_page()
        self.home_controller.ui.home_location_button.on_release = \
            lambda: self.show_location_page()
        self.home_controller.ui.home_geoid_model_button.on_release = \
            lambda: self.show_geoid_model_page()

    def show_levelling_page(self):
        levelling = MainLevellingController()

        try:
            levelling.levelling_file_upload_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(levelling)]
            levelling.levelling_file_upload_controller.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(levelling)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)

            # self.add_widget(pages[page])
            Clock.schedule_once(lambda x: self.general_transition(levelling), 0)

        except:
            pass

    def show_traversing_page(self):
        traversing = MainTraversingController()

        try:
            traversing.traversing_file_upload_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(traversing)]
            traversing.traversing_file_upload_controller.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(traversing)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)

            # self.add_widget(pages[page])
            Clock.schedule_once(lambda x: self.general_transition(traversing), 0)

        except:
            pass

    def show_beardist_page(self):
        beardist = MainBearDistController()

        try:
            beardist.beardist_file_upload_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(beardist)]
            beardist.beardist_file_upload_controller.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(beardist)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)

            # self.add_widget(pages[page])
            Clock.schedule_once(lambda x: self.general_transition(beardist), 0)

        except:
            pass

    def show_levels_adjustment_page(self):
        adjustment = MainAdjustmentController()

        try:
            adjustment.adjustment_file_upload_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(adjustment)]
            adjustment.adjustment_file_upload_controller.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(adjustment)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)

            # self.add_widget(pages[page])
            Clock.schedule_once(lambda x: self.general_transition(adjustment), 0)

        except:
            pass

    def show_coords_adjustment_page(self):
        adjustment = MainCoordsAdjustmentController()

        try:
            adjustment.adjustment_file_upload_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(adjustment)]
            adjustment.adjustment_file_upload_controller.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(adjustment)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)

            # self.add_widget(pages[page])
            Clock.schedule_once(lambda x: self.general_transition(adjustment), 0)

        except:
            pass

    def show_geoid_model_page(self):
        adjustment = MainGeoidModelController()

        try:
            adjustment.geoid_model_training_file_upload_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(adjustment)]
            adjustment.geoid_model_training_file_upload_controller.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(adjustment)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)

            # self.add_widget(pages[page])
            Clock.schedule_once(lambda x: self.general_transition(adjustment), 0)

        except:
            pass

    def show_note_page(self):
        notes = MainNoteController()

        try:
            notes.notes_list_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(notes)]
            notes.notes_list_controller.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(notes)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)

            # self.add_widget(pages[page])
            Clock.schedule_once(lambda x: self.general_transition(notes), 0)

        except:
            pass

    def show_todo_page(self):
        todo = MainTodoController()

        try:
            todo.todos_list_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(todo)]
            todo.todos_list_controller.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(todo)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)
            self.clear_widgets()

            # self.add_widget(pages[page])
            Clock.schedule_once(lambda x: self.general_transition(todo), 0)

        except:
            pass

    def show_about_us_page(self):
        about_us = AboutUsController()

        try:
            about_us.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(about_us)]
            about_us.ui.action_buttons.back_button.on_release = \
                lambda: self.general_back_to_home(about_us)

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)

            Clock.schedule_once(lambda x: self.general_transition(about_us), 0)

        except:
            pass

    def show_location_page(self):
        location = MainLocationController()

        try:
            location.location_map_controller.ui.top_nav.left_action_items[0] = \
                ['arrow-left', lambda x: self.general_back_to_home(location)]

            # Hide the side navbar
            self.home_controller.ui.side_nav.set_state('close')

            self.remove_widget(self.home_controller)
            self.add_widget(location)

            # Clock.schedule_once(lambda x: self.general_transition(location), 0)

        except:
            pass

    def general_transition(self, page):
        anim = Animation(size_hint=(1, 1), duration=0.2)
        self.add_widget(page)
        page.size_hint_y = 0
        anim.start(page)

    def general_back_to_home(self, page):
        try:
            self.remove_widget(page)
            del page
            self.add_widget(self.home_controller)
        except:
            pass

        # self.remove_widget(page)
        # self.add_widget(self.home_controller)


if __name__ == "__main__":
    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            main_home_controller = MainHomeController()
            return main_home_controller


    MainApp().run()