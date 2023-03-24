from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from views.notes.create_new_note_view import CreateNewNoteView

from models.notes.notes import AddNewNote


class CreateNewNoteController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget

        self.ui = CreateNewNoteView()
        self.add_widget(self.ui)

        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()
        self.ui.action_buttons.next_button.on_release = lambda: self.save_note()

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
        except:
            pass

    def save_note(self):
        cancel_btn = MDFlatButton(text="No")
        continue_btn = MDFlatButton(text="Yes")
        continue_btn.on_release = lambda: continue_save()
        cancel_btn.on_release = lambda: dialog.dismiss()

        dialog = MDDialog(
            text="Save note?",
            buttons=[
                cancel_btn, continue_btn
            ]
        )

        title = self.ui.note_title.text
        body = self.ui.note_body.text

        if str(title).strip() != "":
            dialog.open()

        def continue_save():
            note = AddNewNote()
            note.insert(title, body)
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
            app = CreateNewNoteController(None, None)

            return app

    MainApp().run()