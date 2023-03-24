from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.toolbar import MDTopAppBar

from utils.widgets import AngelaFileUpload
from utils.widgets import AngelaCheckbox
from utils.widgets import AngelaBackNextButtons


class CoordsAdjustmentFileUploadView(MDBoxLayout):
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

        self.file_upload = AngelaFileUpload()
        self.file_upload.size_hint = (1, 0.2)
        self.file_upload.padding = [50, 10, 50, 30]
        self.body_content.add_widget(self.file_upload)

        self.header_checkbutton = AngelaCheckbox("First Row is a header")
        self.header_checkbutton.size_hint = (None, 0.15)
        self.header_checkbutton.width = 400
        self.header_checkbutton.padding = [20, 20, 50, 25]
        self.body_content.add_widget(self.header_checkbutton)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, 0.5),)
        self.action_buttons_layout.padding = [0, 10, 50, 50]
        self.body_content.add_widget(self.action_buttons_layout)

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
            app = CoordsAdjustmentFileUploadView()

            return app

    MainApp().run()