from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar

from utils.widgets import AngelaBackNextButtons
from utils.widgets import AngelaCombobox


class CoordsAdjustmentCalculateView(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)

        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))

        self.add_widget(self.header)
        self.add_widget(self.body)

        ##############################################
        self.top_nav = MDTopAppBar(title="Coordinates Adjustment", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
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
        self.home_bottom_content.height = 510
        self.home_bottom_content.padding = [50, 0, 50, 0]

        self.weight_type_combo = AngelaCombobox("Weight Type", ['W', '1/W', '1/W²'])
        self.weight_type_combo.drop_down_button.set_item("W")
        self.weight_type_combo.size_hint = (None, None)
        self.weight_type_combo.size = (250, 70)
        self.confidence_level_widget = AngelaCombobox("Confidence Level", ["50%", "65%", "80%", "90%",
                                                                           "95%", "98%", "99%"])
        self.confidence_level_widget.drop_down_button.set_item("99%")
        self.confidence_level_widget.size_hint = (None, None)
        self.confidence_level_widget.size = (250, 70)
        # self.checks_checkbutton = AngelaCheckbox("Perform Checks")
        # self.checks_checkbutton.size_hint = (None, None)
        # self.checks_checkbutton.size = (200, 50)
        # self.adjust_checkbutton = AngelaCheckbox("Adjust Reduce Levels")
        # self.adjust_checkbutton.size_hint = (None, None)
        # self.adjust_checkbutton.size = (200, 50)

        self.home_bottom_content.add_widget(self.weight_type_combo)
        self.home_bottom_content.add_widget(self.confidence_level_widget)
        # self.home_bottom_content.add_widget(self.checks_checkbutton)
        # self.home_bottom_content.add_widget(self.adjust_checkbutton)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, 1),)
        self.action_buttons_layout.padding = [0, 10, 0, 50]
        self.home_bottom_content.add_widget(self.action_buttons_layout)

        self.action_buttons = AngelaBackNextButtons()
        self.action_buttons.size_hint = (0.6, None)
        self.action_buttons.height = 60
        self.action_buttons_layout.add_widget(self.action_buttons)
        ##################################################


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = CoordsAdjustmentCalculateView()

            return app

    MainApp().run()