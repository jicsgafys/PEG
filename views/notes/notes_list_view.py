from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.datatables.datatables import MDDataTable
from kivy.metrics import dp

from utils.widgets import AngelaBackNextButtons
from utils.widgets import AngelaSearchWidget


class NotesListView(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)

        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))

        self.add_widget(self.header)
        self.add_widget(self.body)

        ##############################################
        self.top_nav = MDTopAppBar(title="Notes", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
                                   left_action_items=[['arrow-left', lambda x: None]])
        self.header.add_widget(self.top_nav)
        ##############################################

        ##################################################
        self.body_content = MDBoxLayout(orientation='vertical', size_hint=(1, 1),
                                        padding=[50, 0, 50, 0])
        self.body_content.spacing = 10
        self.body.add_widget(self.body_content)

        self.notes_search_bar = AngelaSearchWidget()
        self.notes_search_bar.size_hint = (1, 0.1)
        self.body_content.add_widget(self.notes_search_bar)

        self.notes_table = MDDataTable(use_pagination=True,
                                       column_data=[
                                           ("ID", dp(30)),
                                           ("TITLE", dp(40)),
                                           ("NOTES", dp(50)),
                                           ("CREATED ON", dp(35)),
                                           ("MODIFIED ON", dp(35)),
                                       ],
                                       check=True
                                       )
        self.notes_table.size_hint = (1, 0.5)
        self.body_content.add_widget(self.notes_table)

        self.notes_commands_layout = MDBoxLayout(size_hint=(1, 0.1), orientation='horizontal',
                                                 spacing=10)
        self.body_content.add_widget(self.notes_commands_layout)

        self.new_note_button = MDIconButton(md_bg_color=(0, 0.4, 1, 1), size_hint=(None, None),
                                            font_style='H6', text_color='white',
                                            theme_text_color='Custom', icon='plus')
        self.notes_commands_layout.add_widget(self.new_note_button)

        self.edit_note_button = MDIconButton(md_bg_color=(0, 0.4, 1, 1), size_hint=(None, None),
                                             font_style='H6', text_color='white',
                                             theme_text_color='Custom', rounded_button=True, icon='pencil')
        self.notes_commands_layout.add_widget(self.edit_note_button)

        self.delete_note_button = MDIconButton(md_bg_color=(0, 0.4, 1, 1), size_hint=(None, None),
                                               font_style='H6', text_color='white',
                                               theme_text_color='Custom', rounded_button=True, icon='delete')
        self.notes_commands_layout.add_widget(self.delete_note_button)

        self.view_note_button = MDIconButton(md_bg_color=(0, 0.4, 1, 1), size_hint=(None, None),
                                             font_style='H6', text_color='white',
                                             theme_text_color='Custom', rounded_button=True, icon='information')
        self.notes_commands_layout.add_widget(self.view_note_button)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, 0.3), )
        self.action_buttons_layout.padding = [0, 10, 0, 50]
        self.body_content.add_widget(self.action_buttons_layout)

        self.action_buttons = AngelaBackNextButtons()
        self.action_buttons.size_hint = (0.32, None)
        self.action_buttons.height = 60
        self.action_buttons.remove_widget(self.action_buttons.next_button)  # Removes the back button
        self.action_buttons_layout.add_widget(self.action_buttons)
        ##################################################


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = NotesListView()

            return app


    MainApp().run()
