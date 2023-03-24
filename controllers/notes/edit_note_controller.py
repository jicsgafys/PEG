from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from views.notes.edit_note_view import EditNoteView

from models.notes.notes import RetrieveOneNote, ModifyNote


class EditNoteController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, note_id):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        self.note_id = note_id

        self.ui = EditNoteView()
        self.add_widget(self.ui)

        self.retrieve_note()

        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()
        self.ui.action_buttons.next_button.on_release = lambda: self.modify_note()

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

    def modify_note(self):
        cancel_btn = MDFlatButton(text="No")
        continue_btn = MDFlatButton(text="Yes")
        continue_btn.on_release = lambda: continue_modify()
        cancel_btn.on_release = lambda: dialog.dismiss()

        dialog = MDDialog(
            text="Modify note?",
            buttons=[
                cancel_btn, continue_btn
            ]
        )
        dialog.open()

        def continue_modify():
            note = ModifyNote()
            title = self.ui.note_title.text
            body = self.ui.note_body.text

            note.modify(self.note_id, title, body)

            self.previous_widget.refresh_page()  # To refresh the page before landing
            self.back_to_previous_widget()

            dialog.dismiss()


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = EditNoteController(None, None, None)

            return app

    MainApp().run()