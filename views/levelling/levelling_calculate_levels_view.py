from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar

from utils.widgets import AngelaBackNextButtons
from utils.widgets import AngelaCombobox
from utils.widgets import AngelaLabeledTwoEntrybox
from utils.widgets import AngelaCheckbox


class LevellingCalculateLevelsView(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)

        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))

        self.add_widget(self.header)
        self.add_widget(self.body)

        ##############################################
        self.top_nav = MDTopAppBar(title="Levelling", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
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
        self.home_bottom_content.height = 455
        self.home_bottom_content.padding = [50, 0, 50, 0]

        self.benchmarks_widget = AngelaLabeledTwoEntrybox("Benchmarks")
        self.benchmarks_widget.first_entry.hint_text = "Initial"
        self.benchmarks_widget.second_entry.hint_text = "Final"
        self.benchmarks_widget.size_hint = (None, None)
        self.benchmarks_widget.size = (250, 70)
        self.reduction_method_combo = AngelaCombobox("Reduction Method", ['HPC', 'R&F'])
        self.reduction_method_combo.drop_down_button.set_item("HPC")
        self.reduction_method_combo.size_hint = (None, None)
        self.reduction_method_combo.size = (250, 70)
        self.misclosure_widget = AngelaLabeledTwoEntrybox("Misclosure [M√n]")
        self.misclosure_widget.first_entry.hint_text = "M Value"
        self.misclosure_widget.sub2.remove_widget(self.misclosure_widget.second_entry)
        self.misclosure_widget.size_hint = (None, None)
        self.misclosure_widget.size = (250, 70)
        self.checks_checkbutton = AngelaCheckbox("Perform Checks")
        self.checks_checkbutton.size_hint = (None, None)
        self.checks_checkbutton.size = (200, 50)
        self.adjust_checkbutton = AngelaCheckbox("Adjust Reduce Levels")
        self.adjust_checkbutton.size_hint = (None, None)
        self.adjust_checkbutton.size = (200, 50)

        self.home_bottom_content.add_widget(self.benchmarks_widget)
        self.home_bottom_content.add_widget(self.reduction_method_combo)
        self.home_bottom_content.add_widget(self.misclosure_widget)
        # self.home_bottom_content.add_widget(self.checks_checkbutton)
        # self.home_bottom_content.add_widget(self.adjust_checkbutton)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, None),)
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
            app = LevellingCalculateLevelsView()

            return app

    MainApp().run()