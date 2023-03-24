from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.toolbar import MDTopAppBar

from utils.widgets import AngelaBackNextButtons

from utils.paths import ICONS_FOLDER_PATH


class AboutUsView(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)

        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))

        self.add_widget(self.header)
        self.add_widget(self.body)

        ##############################################
        self.top_nav = MDTopAppBar(title="About Us", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
                                   left_action_items=[['arrow-left', lambda x: None]])
        self.header.add_widget(self.top_nav)
        ##############################################

        ##################################################
        self.body_content = MDBoxLayout(orientation='vertical', size_hint=(1, 1),
                                        padding=[50, 0, 50, 0])
        self.body.add_widget(self.body_content)

        self.body_content_header = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.body_content_header.spacing = 10
        self.body_content_header.padding = [0, 0, 0, 20]
        self.body_content_body = MDBoxLayout(orientation='vertical', size_hint=(1, 0.15))
        self.body_content_body.spacing = 20
        self.body_content_footer = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.6))

        self.body_content.add_widget(self.body_content_header)
        self.body_content.add_widget(self.body_content_body)
        self.body_content.add_widget(self.body_content_footer)

        self.project_logo = Image(source=ICONS_FOLDER_PATH + "app_logo.png", size_hint=(None, None))
        self.project_logo.size = (100, 100)
        self.project_title = MDLabel(text="\nPeg  0.1", size_hint=(1, 1), font_style="H5", halign='left',
                                     valign='center')
        self.body_content_header.add_widget(self.project_logo)
        self.body_content_header.add_widget(self.project_title)

        project_info1_label_text = "Powered by:  [i][b][size=14]PROJECT 1 - GROUP 2, 2023 CLASS KNUST." \
                                   "[/size][/b][/i]"
        project_info2_label_text = "Built with: Python & KivyMD." \
                                   "\nCopyright @2023 Peg."
        self.project_info1_label = MDLabel(text=project_info1_label_text, font_style="Subtitle1", halign='left',
                                           size_hint=(1, 0.5), markup=True)
        self.project_info2_label = MDLabel(text=project_info2_label_text, halign='left',
                                           size_hint=(1, 0.3), markup=True)
        self.body_content_body.add_widget(self.project_info1_label)
        self.body_content_body.add_widget(self.project_info2_label)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, 0.5),)
        self.action_buttons_layout.padding = [0, 10, 0, 50]
        self.body_content_footer.add_widget(self.action_buttons_layout)

        self.action_buttons = AngelaBackNextButtons()
        self.action_buttons.size_hint = (0.32, None)
        self.action_buttons.height = 60
        self.action_buttons.remove_widget(self.action_buttons.next_button)
        self.action_buttons_layout.add_widget(self.action_buttons)
        ##################################################


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = AboutUsView()

            return app

    MainApp().run()