from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.clock import Clock

from controllers.notes.edit_note_controller import EditNoteController
from controllers.notes.create_new_note_controller import CreateNewNoteController
from controllers.notes.notes_list_controller import NotesListController
from controllers.notes.read_note_controller import ReadNoteController


class MainNoteController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        # Default home screen for the page
        self.notes_list_controller = NotesListController()
        self.add_widget(self.notes_list_controller)

        # Bindings
        self.notes_list_controller.ui.new_note_button.on_release = lambda: self.show_create_new_note()
        self.notes_list_controller.ui.edit_note_button.on_release = lambda: self.show_edit_note()
        self.notes_list_controller.ui.view_note_button.on_release = lambda: self.show_read_note()

    def show_create_new_note(self):

        try:
            create_new_note_controller = CreateNewNoteController(self, self.notes_list_controller)
            Clock.schedule_once(lambda x: transition(), 0)
            self.remove_widget(self.notes_list_controller)

        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.add_widget(create_new_note_controller)
            create_new_note_controller.size_hint_y = 0
            anim.start(create_new_note_controller)

    def show_edit_note(self):
        try:
            sel_note = self.notes_list_controller.ui.notes_table.get_row_checks()  # [[], []]
            if sel_note:
                if sel_note[0]:
                    _note_id = sel_note[0][0]
                    edit_note_controller = EditNoteController(self, self.notes_list_controller, _note_id)
                    Clock.schedule_once(lambda x: transition(), 0)
                    self.remove_widget(self.notes_list_controller)
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.add_widget(edit_note_controller)
            edit_note_controller.size_hint_y = 0
            anim.start(edit_note_controller)

    def show_read_note(self):
        try:
            sel_note = self.notes_list_controller.ui.notes_table.get_row_checks()
            if sel_note:
                if sel_note[0]:
                    _note_id = sel_note[0][0]
                    view_note_controller = ReadNoteController(self, self.notes_list_controller, _note_id)
                    Clock.schedule_once(lambda x: transition(), 0)
                    self.remove_widget(self.notes_list_controller)
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.add_widget(view_note_controller)
            view_note_controller.size_hint_y = 0
            anim.start(view_note_controller)


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = MainNoteController()

            return app


    MainApp().run()
