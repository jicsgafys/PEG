from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield.textfield import MDTextField

from utils.widgets import AngelaBackNextButtons


class CreateNewNoteView(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)

        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))

        self.add_widget(self.header)
        self.add_widget(self.body)

        ##############################################
        self.top_nav = MDTopAppBar(title="New Note", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
                                   left_action_items=[['arrow-left', lambda x: None]])
        self.header.add_widget(self.top_nav)
        ##############################################

        ##################################################
        self.body_content = MDBoxLayout(orientation='vertical', size_hint=(1, 1),
                                        padding=[50, 0, 50, 0])
        self.body_content.spacing = 10
        self.body.add_widget(self.body_content)

        self.note_title = MDTextField(hint_text="Title")
        self.note_title.size_hint = (1, 0.1)
        self.body_content.add_widget(self.note_title)

        self.note_body = MDTextField(hint_text="Body", multiline=True)
        self.note_body.size_hint = (1, 0.2)
        self.body_content.add_widget(self.note_body)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, 0.5),)
        self.action_buttons_layout.padding = [0, 10, 0, 50]
        self.body_content.add_widget(self.action_buttons_layout)

        self.action_buttons = AngelaBackNextButtons()
        self.action_buttons.size_hint = (0.6, None)
        self.action_buttons.height = 60
        # self.action_buttons.remove_widget(self.action_buttons.back_button)  # Removes the back button
        self.action_buttons.next_button.text = "Save"  # Changes the name of the next button to 'Save'
        self.action_buttons_layout.add_widget(self.action_buttons)
        ##################################################


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = CreateNewNoteView()

            return app

    MainApp().run()