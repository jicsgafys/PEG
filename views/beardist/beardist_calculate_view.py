from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar

from utils.widgets import AngelaBackNextButtons, AngelaCombobox
from utils.widgets import AngelaCheckbox


class BearDistCalculateLevelsView(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)

        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))

        self.add_widget(self.header)
        self.add_widget(self.body)

        ##############################################
        self.top_nav = MDTopAppBar(title="Bear & Dist", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
                                   left_action_items=[['arrow-left', lambda x: None]])
        self.header.add_widget(self.top_nav)
        ##############################################

        ##################################################
        self.body_content = MDBoxLayout(orientation='vertical', size_hint=(1, 1),
                                        padding=[0, 0, 0, 0])
        self.body.add_widget(self.body_content)

        self.home_top_layout = MDBoxLayout(size_hint=(1, .15), padding=[50, 0, 50, 0])
        self.body_content.add_widget(self.home_top_layout)

        self.body_title_label = MDLabel(text="Computation Settings", size_hint=(1, 1), font_style="H6")
        self.home_top_layout.add_widget(self.body_title_label)

        self.home_bottom_layout = MDScrollView(size_hint=(1, .8))
        self.body_content.add_widget(self.home_bottom_layout)

        self.home_bottom_content = MDBoxLayout(size_hint=(1, None), orientation='vertical',
                                               spacing=40)
        self.home_bottom_layout.add_widget(self.home_bottom_content)
        self.home_bottom_content.height = 480
        self.home_bottom_content.padding = [50, 0, 50, 0]

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.output_angles_layout = MDBoxLayout(orientation='vertical', size_hint=(None, None),
                                                spacing=20)
        self.output_angles_layout.size = (200, 60)
        self.home_bottom_content.add_widget(self.output_angles_layout)

        self.output_angles_format_combo = AngelaCombobox("Output Angle Format",
                                                         ['Deci Deg', 'Deg Min Sec'])
        self.output_angles_format_combo.drop_down_button.set_item("Deci Deg")
        self.output_angles_format_combo.size_hint = (None, None)
        self.output_angles_format_combo.size = (250, 50)

        self.output_coords_separator_widget = AngelaCombobox(
            "Format Separator", ['space', ',,', ',', "'", "\"", '/', '|', '\\'])
        self.output_coords_separator_widget.title_label.font_size = 13
        self.output_coords_separator_widget.drop_down_button.set_item('space')
        self.output_coords_separator_widget.size_hint = (None, None)
        self.output_coords_separator_widget.size = (150, 40)

        self.output_angles_layout.add_widget(self.output_angles_format_combo)
        # self.output_coords_layout.add_widget(self.output_coords_separator_widget)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        self.included_angle_checkbutton = AngelaCheckbox("Calculate Included Angle")
        self.included_angle_checkbutton.size_hint = (None, None)
        self.included_angle_checkbutton.size = (200, 50)
        self.excluded_angle_checkbutton = AngelaCheckbox("Calculate Excluded Angle")
        self.excluded_angle_checkbutton.size_hint = (None, None)
        self.excluded_angle_checkbutton.size = (200, 50)

        # self.home_bottom_content.add_widget(self.included_angle_checkbutton)
        # self.home_bottom_content.add_widget(self.excluded_angle_checkbutton)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, 1),)
        self.action_buttons_layout.padding = [0, 10, 0, 50]
        self.home_bottom_content.add_widget(self.action_buttons_layout)

        self.action_buttons = AngelaBackNextButtons()
        self.action_buttons.size_hint = (0.6, None)
        self.action_buttons.height = 60
        self.action_buttons_layout.add_widget(self.action_buttons)
        ##################################################
        self.output_coords_trigger()

    def output_coords_trigger(self):
        menu_items = []
        for item in ['Deci Deg', 'Deg Min Sec']:
            item_widget = {
                'viewclass': "OneLineListItem",
                'text': str(item),
                "height": dp(56),
                'on_release': lambda x=str(item): set_item(x)
            }
            menu_items.append(item_widget)

        self.output_angles_format_combo.drop_down_menu.items = menu_items

        def set_item(text_item):
            if str(text_item) == "Deci Deg":
                self.output_angles_layout.remove_widget(self.output_coords_separator_widget)
                self.output_angles_layout.size = (200, 60)
            else:
                self.output_angles_layout.add_widget(self.output_coords_separator_widget)
                self.output_angles_layout.size = (200, 120)

            self.output_angles_format_combo.drop_down_button.set_item(text_item)
            self.output_angles_format_combo.drop_down_menu.dismiss()


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = BearDistCalculateLevelsView()

            return app

    MainApp().run()