from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog.dialog import MDDialog
from kivy.clock import Clock

from views.notes.notes_list_view import NotesListView

from models.notes.notes import RetrieveAllNotes, SearchForNote, DeleteNote


class NotesListController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        self.ui = NotesListView()
        self.add_widget(self.ui)

        self.is_search = False
        self.retrieved_data = {}

        #
        Clock.schedule_once(lambda x: self.refresh_page(), 2)
        # self.refresh_page()

        #
        self.ui.delete_note_button.on_press = \
            lambda: self.delete_notes(self.ui.notes_table.get_row_checks())
        self.ui.notes_search_bar.search_button.on_release = lambda: self.search_for_notes()
        self.ui.notes_search_bar.refresh_button.on_release = lambda: self.refresh_page()

        #

    def refresh_page(self):
        self.is_search = False
        self.ui.notes_table.row_data = []
        self.retrieve_notes()
        self.display_notes()

    def display_notes(self):
        # table_header = ("ID", 'TITLE', 'NOTE', 'CREATED ON', 'MODIFIED ON')
        header = self.retrieved_data['header']
        body = self.retrieved_data['body']

        # data
        display_data = []

        for line in body:
            _id = line[header.index('ID')]
            _title = line[header.index('TITLE')]
            _note = line[header.index('NOTES')]
            _created_on = ('calendar', line[header.index('CREATED ON')])
            _modified_on = ('calendar', line[header.index('MODIFIED ON')])

            display_data.append([_id, _title, _note, _created_on, _modified_on])

        self.ui.notes_table.row_data = display_data

    def retrieve_notes(self):
        notes = RetrieveAllNotes()
        header = notes.get_results_header()
        body = notes.get_results_body()

        self.retrieved_data = {'header': header, 'body': body}

    def delete_notes(self, sel_data):
        cancel_btn = MDFlatButton(text="No")
        continue_btn = MDFlatButton(text="Yes")
        continue_btn.on_release = lambda: continue_delete()
        cancel_btn.on_release = lambda: dialog.dismiss()

        dialog = MDDialog(
            text="Delete note?",
            buttons=[
                cancel_btn, continue_btn
            ]
        )
        if sel_data:
            dialog.open()

        def continue_delete():
            _del_model = DeleteNote()

            for data in sel_data:
                if data:
                    _id = data[0]
                    _del_model.delete_data(_id)

            self.refresh_page()
            dialog.dismiss()

    def search_for_notes(self):
        self.is_search = True

        search_term = self.ui.notes_search_bar.search_input_entry.text
        notes = SearchForNote()
        header = notes.get_results_header()
        body = notes.get_results_body(search_term)

        self.retrieved_data = {'header': header, 'body': body}

        self.display_notes()


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = NotesListController()

            return app


    MainApp().run()
