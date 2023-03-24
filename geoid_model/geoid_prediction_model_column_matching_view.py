from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar

from utils.widgets import AngelaBackNextButtons
from utils.widgets import AngelaCombobox


class GeoidModelPredictionColumnMatchingView(MDBoxLayout):
    def __init__(self, column_header):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.column_header = column_header

        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))

        self.add_widget(self.header)
        self.add_widget(self.body)

        ##############################################
        self.top_nav = MDTopAppBar(title="Geoid Modelling", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
                                   left_action_items=[['arrow-left', lambda x: None]])
        self.header.add_widget(self.top_nav)
        ##############################################

        ##################################################
        self.body_content = MDBoxLayout(orientation='vertical', size_hint=(1, 1),
                                        padding=[0, 0, 0, 0])
        self.body.add_widget(self.body_content)

        self.home_top_layout = MDBoxLayout(size_hint=(1, .15), padding=[50, 0, 50, 0])
        self.body_content.add_widget(self.home_top_layout)

        self.body_title_label = MDLabel(text="Column Matching [Prediction]", size_hint=(1, 1), font_style="H6")
        self.home_top_layout.add_widget(self.body_title_label)

        self.home_bottom_layout = MDScrollView(size_hint=(1, .8))
        self.body_content.add_widget(self.home_bottom_layout)

        self.home_bottom_content = MDBoxLayout(size_hint=(1, None), orientation='vertical',
                                               spacing=40)
        self.home_bottom_layout.add_widget(self.home_bottom_content)
        self.home_bottom_content.height = 600
        self.home_bottom_content.padding = [50, 0, 50, 0]

        self.station_combo = AngelaCombobox("Station", self.column_header)
        self.station_combo.drop_down_button.set_item(self.column_header[0])
        self.station_combo.size_hint = (None, None)
        self.station_combo.size = (250, 70)
        self.gps_easting_combo = AngelaCombobox("GPS Easting", self.column_header)
        self.gps_easting_combo.drop_down_button.set_item(self.column_header[0])
        self.gps_easting_combo.size_hint = (None, None)
        self.gps_easting_combo.size = (250, 70)
        self.gps_northing_combo = AngelaCombobox("GPS Northing", self.column_header)
        self.gps_northing_combo.drop_down_button.set_item(self.column_header[0])
        self.gps_northing_combo.size_hint = (None, None)
        self.gps_northing_combo.size = (250, 70)
        self.gps_height_combo = AngelaCombobox("GPS Height", self.column_header)
        self.gps_easting_combo.drop_down_button.set_item(self.column_header[0])
        self.gps_height_combo.size_hint = (None, None)
        self.gps_height_combo.size = (250, 70)

        self.home_bottom_content.add_widget(self.station_combo)
        self.home_bottom_content.add_widget(self.gps_easting_combo)
        self.home_bottom_content.add_widget(self.gps_northing_combo)
        self.home_bottom_content.add_widget(self.gps_height_combo)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, 1),)
        self.action_buttons_layout.padding = [0, 10, 0, 50]
        self.home_bottom_content.add_widget(self.action_buttons_layout)

        self.action_buttons = AngelaBackNextButtons()
        self.action_buttons.size_hint = (0.6, None)
        self.action_buttons.height = 60
        self.action_buttons_layout.add_widget(self.action_buttons)
        ##################################################

    def reset_combo_drop_down_items(self):
        combos = (self.station_combo, self.gps_easting_combo,
                  self.gps_height_combo, self.gps_northing_combo)
        for combo in combos:
            menu_items = []
            for item in self.column_header:
                item_widget = {
                    'viewclass': "OneLineListItem",
                    'text': str(item),
                    "height": dp(56),
                    'on_release': lambda y=combo, x=str(item): set_item(y, x)
                }
                menu_items.append(item_widget)

            combo.drop_down_menu.items = menu_items

            def set_item(combobox, text_item):
                combobox.drop_down_button.set_item(text_item)
                combobox.drop_down_menu.dismiss()


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