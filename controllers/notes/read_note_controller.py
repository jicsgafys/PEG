from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from views.notes.read_note_view import ReadNoteView

from models.notes.notes import RetrieveOneNote


class ReadNoteController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, note_id):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        self.note_id = note_id

        self.ui = ReadNoteView()
        self.add_widget(self.ui)

        self.retrieve_note()

        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
        except:
            pass

    def retrieve_note(self):
        note = RetrieveOneNote()
        header = note.get_results_header()
        body = note.get_results_body(self.note_id)

        title = body[header.index("TITLE")]
        body = body[header.index("NOTES")]

        # Filling the widgets
        self.ui.note_title.set_text(self.ui.note_title, str(title))
        self.ui.note_body.set_text(self.ui.note_body, str(body))

        # Making the fields readonly
        self.ui.note_title.readonly = True
        self.ui.note_body.readonly = True


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = ReadNoteController(None, None, 1)

            return app

    MainApp().run()