from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from utils.paths import ICONS_FOLDER_PATH

from models.todos.todos import RetrieveAllTodos, DeleteTodo, SearchForTodo
from views.todos.todos_list_view import TodosListView


class TodosListController(MDScreen):
    def __init__(self):
        super().__init__()
        self.ui = TodosListView()
        self.add_widget(self.ui)

        self.is_search = False
        self.retrieved_data = {}

        #
        Clock.schedule_once(lambda x: self.refresh_page(), 2)
        # self.refresh_page()

        #
        self.ui.delete_todo_button.on_press = \
            lambda: self.delete_todos(self.ui.todos_table.get_row_checks())
        self.ui.todos_search_bar.search_button.on_release = lambda: self.search_for_todos()
        self.ui.todos_search_bar.refresh_button.on_release = lambda: self.refresh_page()

        #

    def refresh_page(self):
        self.is_search = False
        self.ui.todos_table.row_data = []
        self.retrieve_todos()
        self.display_todos()

    def display_todos(self):
        # table_header = ['ID', 'TASK', 'DESCRIPTION', 'ASSIGNEES', 'START DATE',
        #                 'EXPECTED END DATE', 'STATUS', 'ACTUAL END DATE', 'CREATED ON',
        #                 'MODIFIED ON']
        header = self.retrieved_data['header']
        body = self.retrieved_data['body']

        _initial_icon = ICONS_FOLDER_PATH + 'initial.png'
        _progress_icon = ICONS_FOLDER_PATH + 'progress.png'
        _finished_icon = ICONS_FOLDER_PATH + 'finished.png'

        # data
        display_data = []

        for line in body:
            _id = line[header.index('ID')]
            _task = line[header.index('TASK')]
            _description = line[header.index('DESCRIPTION')]
            _assignees = line[header.index('ASSIGNEES')]
            _start_on = ('calendar', line[header.index('START DATE')])
            _expected_end_on = ('calendar', line[header.index('EXPECTED END DATE')])
            _status = line[header.index('STATUS')]
            if int(_status) == 0:
                _status = (_initial_icon, str(_status) + "%")
            elif int(_status) == 100:
                _status = (_finished_icon, str(_status) + "%")
            else:
                _status = (_progress_icon, str(_status) + "%")
            _actual_end_on = ('calendar', line[header.index('ACTUAL END DATE')])
            _created_on = ('calendar', line[header.index('CREATED ON')])
            _modified_on = ('calendar', line[header.index('MODIFIED ON')])

            display_data.append([_id, _task, _description, _assignees, _start_on, _expected_end_on,
                                 _status, _actual_end_on, _created_on, _modified_on])

        self.ui.todos_table.row_data = display_data

    def retrieve_todos(self):
        todos = RetrieveAllTodos()
        header = todos.get_results_header()
        body = todos.get_results_body()

        self.retrieved_data = {'header': header, 'body': body}

    def delete_todos(self, sel_data):
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
            _del_model = DeleteTodo()

            for data in sel_data:
                if data:
                    _id = data[0]
                    _del_model.delete_data(_id)

            self.refresh_page()
            dialog.dismiss()

    def search_for_todos(self):
        self.is_search = True

        search_term = self.ui.todos_search_bar.search_input_entry.text
        todos = SearchForTodo()
        header = todos.get_results_header()
        body = todos.get_results_body(search_term)

        self.retrieved_data = {'header': header, 'body': body}

        self.display_todos()


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = TodosListController()

            return app


    MainApp().run()
