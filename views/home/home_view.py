from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer.navigationdrawer import MDNavigationDrawer, \
    MDNavigationDrawerHeader, MDNavigationDrawerItem, MDNavigationDrawerMenu
from kivymd.uix.carousel import MDCarousel
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.toolbar.toolbar import MDTopAppBar
from kivymd.uix.button.button import MDFlatButton
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window
from kivymd.uix.pickers.timepicker import MDTimePicker
from datetime import datetime

# 360 X 640

from utils.widgets import AngelaCard
from utils.paths import IMAGES_FOLDER_PATH
from utils.paths import ICONS_FOLDER_PATH


class HomeView(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'

        ########################################
        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))
        self.footer = MDAnchorLayout(anchor_y='bottom', size_hint=(1, 0.1))

        self.add_widget(self.header)
        self.add_widget(self.body)
        self.add_widget(self.footer)
        #############################################

        ##############################################
        self.top_nav = MDTopAppBar(title="Peg", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
                                   left_action_items=[['menu', lambda x: self.toggle_side_navbar()]])
        self.header.add_widget(self.top_nav)
        ##############################################

        ################################################
        self.home_content = MDBoxLayout(size_hint=(1, 1), orientation='vertical')
        self.body.add_widget(self.home_content)

        self.home_top_layout = MDBoxLayout(size_hint=(1, 0.4), padding=[10, 10, 10, 0])
        self.home_bottom_layout = MDScrollView(size_hint=(1, .6))

        self.home_content.add_widget(self.home_top_layout)
        self.home_content.add_widget(self.home_bottom_layout)

        self.home_carousel1 = MDCarousel(size_hint=(1, 1))
        self.home_top_layout.add_widget(self.home_carousel1)

        self.card1 = AngelaCard(IMAGES_FOLDER_PATH + "digital_theodolite.jpeg", "Digital Theodolite")
        self.card2 = AngelaCard(IMAGES_FOLDER_PATH + "surveyors_tape.jpeg", "Surveyors Tape")
        self.card3 = AngelaCard(IMAGES_FOLDER_PATH + "handheld_gps.jpeg", "Handheld GPS")
        self.card4 = AngelaCard(IMAGES_FOLDER_PATH + "tape_measure.jpeg", "Tape Measure")
        self.card5 = AngelaCard(IMAGES_FOLDER_PATH + "tripod.jpeg", "Tripod")
        self.card6 = AngelaCard(IMAGES_FOLDER_PATH + "total_station.jpeg", "Total Station")
        self.card7 = AngelaCard(IMAGES_FOLDER_PATH + "gps_receivers.jpeg", "GPS receiver")
        self.card8 = AngelaCard(IMAGES_FOLDER_PATH + "tape_measure.jpeg", "Tape Measure")
        self.card9 = AngelaCard(IMAGES_FOLDER_PATH + "level_instrument.jpeg", "Level Instrument")

        self.home_carousel1.add_widget(self.card1)
        self.home_carousel1.add_widget(self.card2)
        self.home_carousel1.add_widget(self.card3)
        self.home_carousel1.add_widget(self.card4)
        self.home_carousel1.add_widget(self.card5)
        self.home_carousel1.add_widget(self.card6)
        self.home_carousel1.add_widget(self.card7)
        self.home_carousel1.add_widget(self.card8)
        self.home_carousel1.add_widget(self.card9)

        self.home_buttons_layout = MDStackLayout(spacing=10, padding=10, size_hint=(1, None),
                                                 height=300)
        self.home_bottom_layout.add_widget(self.home_buttons_layout)

        self.home_levelling_button = MDFlatButton(text="Levelling", font_size=18, size_hint=(0.5, 0.25),
                                                  md_bg_color=(0.2, 0.6, 1, 1), text_color='white',
                                                  theme_text_color='Custom')
        self.home_traversing_button = MDFlatButton(text="Traversing", font_size=18, size_hint=(0.5, 0.25),
                                                   md_bg_color=(0.2, 0.6, 1, 1), text_color='white',
                                                   theme_text_color='Custom')
        self.home_levels_adjustment_button = MDFlatButton(
            text="Levels Adjustment", font_size=18, size_hint=(0.5, 0.25), md_bg_color=(0.2, 0.6, 1, 1),
            text_color='white', theme_text_color='Custom')
        self.home_beardist_button = MDFlatButton(text="Bear & Dist", font_size=18, size_hint=(0.5, 0.25),
                                                 md_bg_color=(0.2, 0.6, 1, 1), text_color='white',
                                                 theme_text_color='Custom')
        self.home_geoid_model_button = MDFlatButton(
            text="Geoid Modelling", font_size=18, size_hint=(0.5, 0.25), md_bg_color=(0.2, 0.6, 1, 1),
            text_color='white', theme_text_color='Custom')
        self.home_coords_adjustment_button = MDFlatButton(
            text="Coords Adjustment", font_size=18, size_hint=(0.5, 0.25), md_bg_color=(0.2, 0.6, 1, 1),
            text_color='white', theme_text_color='Custom')
        self.home_todo_button = MDFlatButton(text="Todo", font_size=18, size_hint=(0.5, 0.25),
                                             md_bg_color=(0.2, 0.6, 1, 1), text_color='white',
                                             theme_text_color='Custom')
        self.home_note_button = MDFlatButton(text="Notes", font_size=18, size_hint=(0.5, 0.25),
                                             md_bg_color=(0.2, 0.6, 1, 1), text_color='white',
                                             theme_text_color='Custom')
        self.home_location_button = MDFlatButton(text="Location", font_size=18, size_hint=(0.5, 0.25),
                                                 md_bg_color=(0.2, 0.6, 1, 1), text_color='white',
                                                 theme_text_color='Custom')
        self.home_help_button = MDFlatButton(text="Help", font_size=18, size_hint=(0.5, 0.25),
                                             md_bg_color=(0.2, 0.6, 1, 1), text_color='white',
                                             theme_text_color='Custom')
        self.home_about_button = MDFlatButton(text="About Us", size_hint=(0.5, 0.25),
                                              md_bg_color=(0.2, 0.6, 1, 1), text_color='white',
                                              theme_text_color='Custom', font_size=18)

        self.home_buttons_layout.add_widget(self.home_levelling_button)
        # self.home_buttons_layout.add_widget(self.home_traversing_button)
        self.home_buttons_layout.add_widget(self.home_levels_adjustment_button)
        self.home_buttons_layout.add_widget(self.home_beardist_button)
        self.home_buttons_layout.add_widget(self.home_geoid_model_button)
        self.home_buttons_layout.add_widget(self.home_todo_button)
        self.home_buttons_layout.add_widget(self.home_note_button)
        self.home_buttons_layout.add_widget(self.home_location_button)
        # self.home_buttons_layout.add_widget(self.home_help_button)
        self.home_buttons_layout.add_widget(self.home_about_button)
        ################################################

        ##############################################
        self.side_nav = MDNavigationDrawer(orientation='vertical', elevation=5, size_hint=(1, 1))
        self.side_nav.set_state('close')
        self.body.add_widget(self.side_nav)

        app_icon_full_path = ICONS_FOLDER_PATH + "app_logo.png"
        self.side_nav_icon = Image(source=app_icon_full_path, size_hint=(0.5, 0.25))
        self.side_nav_header = MDNavigationDrawerHeader(title="", title_font_size='25sp',
                                                        padding=[30, 0, 10, 10], title_color='brown', spacing=5,
                                                        )
        self.side_nav_body = MDNavigationDrawerMenu()

        self.side_nav.add_widget(self.side_nav_icon)
        # self.side_nav.add_widget(self.side_nav_header)
        self.side_nav.add_widget(self.side_nav_body)

        # self.home_nav_button = MDNavigationDrawerItem(text="Home", font_style='Subtitle1')
        self.levelling_nav_button = MDNavigationDrawerItem(text="Levelling", font_style='Subtitle1')
        self.traversing_nav_button = MDNavigationDrawerItem(text="Traversing", font_style="Subtitle1")
        self.levels_adjustment_nav_button = MDNavigationDrawerItem(text="Levels Adjustment", font_style="Subtitle1")
        self.coords_adjustment_nav_button = MDNavigationDrawerItem(text="Coords Adjustment", font_style="Subtitle1")
        self.beardist_nav_button = MDNavigationDrawerItem(text="Bear & Dist", font_style="Subtitle1")
        self.geoid_model_nav_button = MDNavigationDrawerItem(text="Geoid Modelling", font_style="Subtitle1")
        self.todo_nav_button = MDNavigationDrawerItem(text="Todo", font_style="Subtitle1")
        self.note_nav_button = MDNavigationDrawerItem(text="Notes", font_style="Subtitle1")
        self.location_nav_button = MDNavigationDrawerItem(text="Location", font_style="Subtitle1")
        self.help_nav_button = MDNavigationDrawerItem(text="Help", font_style="Subtitle1")
        self.about_nav_button = MDNavigationDrawerItem(text="About Us", font_style="Subtitle1")

        # self.side_nav_body.add_widget(self.home_nav_button)
        self.side_nav_body.add_widget(self.levelling_nav_button)
        # self.side_nav_body.add_widget(self.traversing_nav_button)
        self.side_nav_body.add_widget(self.levels_adjustment_nav_button)
        self.side_nav_body.add_widget(self.coords_adjustment_nav_button)
        self.side_nav_body.add_widget(self.geoid_model_nav_button)
        self.side_nav_body.add_widget(self.beardist_nav_button)
        self.side_nav_body.add_widget(self.todo_nav_button)
        self.side_nav_body.add_widget(self.note_nav_button)
        self.side_nav_body.add_widget(self.location_nav_button)
        # self.side_nav_body.add_widget(self.help_nav_button)
        self.side_nav_body.add_widget(self.about_nav_button)
        ################################################

        ####################################################
        self.bottom_nav = MDTopAppBar(md_bg_color=(0.2, 0.5, 0.9, 1),
                                      right_action_items=[['clock', lambda x: self.show_current_time()],
                                                          ['calendar', lambda x: self.show_current_date()]])
        self.footer.add_widget(self.bottom_nav)
        ####################################################

        #####################################################
        self.time_dialog = MDTimePicker()
        self.date_dialog = MDDatePicker()
        #########################################################

    def toggle_side_navbar(self):
        if self.side_nav.state == "open":
            self.side_nav.set_state('close')

        else:
            self.side_nav.set_state('open')

    def show_current_time(self):
        # 2023-03-04 21:59:25.066306 to 21:59:25.066306 to [21, 59, 25.066306]
        split_time = str(datetime.now()).split(" ")[-1].split(":")
        time = str(split_time[0]) + ":" + str(split_time[1]) + ":" + \
               str(int(float(split_time[2])))  # 21:59:25.066306

        time_object = datetime.strptime(time, '%H:%M:%S').time()
        self.time_dialog.set_time(time_object)
        self.time_dialog.title = "Current Time"
        self.time_dialog.set_disabled(True)
        self.time_dialog.open()

    def show_current_date(self):
        # 2023-03-04 21:59:25.066306 to 2023-03-04 to [2023, 03, 04]
        split_date = str(datetime.now()).split(" ")[0]

        self.date_dialog.set_text_full_date(split_date[0], split_date[1], split_date[2],
                                            orientation='horizontal')
        self.date_dialog.title = "Current Date"
        self.date_dialog.set_disabled(True)
        self.date_dialog.open()


if __name__ == "__main__":
    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            homeview = HomeView()
            return homeview


    MainApp().run()
