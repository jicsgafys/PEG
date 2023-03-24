from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker

from models.todos.todos import RetrieveOneTodo
from views.todos.view_todo_view import ViewTodoView


class ViewTodoController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget, todo_id):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget
        self.todo_id = todo_id

        self.ui = ViewTodoView()
        self.add_widget(self.ui)

        self.retrieve_todo()

        self.ui.todo_task_start_date.select_button.on_release = lambda: self.set_start_date_date()
        self.ui.todo_task_expected_end_date.select_button.on_release = lambda: self.set_expected_end_date_date()
        self.ui.todo_task_actual_end_date.select_button.on_release = lambda: self.set_actual_end_date_date()
        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()

    def back_to_previous_widget(self):
        try:
            self.main_container_widget.remove_widget(self)
            self.main_container_widget.add_widget(self.previous_widget)
        except:
            pass

    def set_start_date_date(self):
        date_dialog = MDDatePicker()

        date_dialog.title = "Select Date"
        date_dialog.open()

        date_dialog.on_ok_button_pressed = lambda x=date_dialog: save_date(x)

        def save_date(dialog):
            _date = f'{dialog.sel_year}-{dialog.sel_month}-{dialog.sel_day}'
            self.ui.todo_task_start_date.date_input_entry.set_text(self.ui, _date)
            date_dialog.on_cancel()

    def set_expected_end_date_date(self):
        date_dialog = MDDatePicker()

        date_dialog.title = "Select Date"
        date_dialog.open()

        date_dialog.on_ok_button_pressed = lambda x=date_dialog: save_date(x)

        def save_date(dialog):
            _date = f'{dialog.sel_year}-{dialog.sel_month}-{dialog.sel_day}'
            self.ui.todo_task_expected_end_date.date_input_entry.set_text(self.ui, _date)
            date_dialog.on_cancel()

    def set_actual_end_date_date(self):
        date_dialog = MDDatePicker()

        date_dialog.title = "Select Date"
        date_dialog.open()

        date_dialog.on_ok_button_pressed = lambda x=date_dialog: save_date(x)

        def save_date(dialog):
            _date = f'{dialog.sel_year}-{dialog.sel_month}-{dialog.sel_day}'
            self.ui.todo_task_actual_end_date.date_input_entry.set_text(self.ui, _date)
            date_dialog.on_cancel()

    def retrieve_todo(self):
        note = RetrieveOneTodo()
        header = note.get_results_header()
        body = note.get_results_body(self.todo_id)

        #  ['ID', 'TASK', 'DESCRIPTION', 'ASSIGNEES', 'START DATE',
        #                 'EXPECTED END DATE', 'STATUS', 'ACTUAL END DATE', 'CREATED ON',
        #                 'MODIFIED ON']
        title = body[header.index("TASK")]
        description = body[header.index("DESCRIPTION")]
        assignees = body[header.index("ASSIGNEES")]
        start_date = body[header.index("START DATE")]
        expected_end_date = body[header.index("EXPECTED END DATE")]
        status = body[header.index("STATUS")]
        actual_end_date = body[header.index("ACTUAL END DATE")]

        #
        self.ui.todo_task_start_date.date_input_entry.disabled = False
        self.ui.todo_task_expected_end_date.date_input_entry.disabled = False
        self.ui.todo_task_expected_end_date.date_input_entry.disabled = False

        # Filling the widgets
        self.ui.todo_task_title.set_text(self.ui.todo_task_title, str(title))
        self.ui.todo_task_body.set_text(self.ui.todo_task_body, str(description))
        self.ui.todo_task_assignees.set_text(self.ui.todo_task_assignees, str(assignees))
        self.ui.todo_task_start_date.date_input_entry.set_text(
            self.ui.todo_task_start_date.date_input_entry, str(start_date))
        self.ui.todo_task_expected_end_date.date_input_entry.set_text(
            self.ui.todo_task_expected_end_date.date_input_entry, str(expected_end_date))
        self.ui.percent_progress.drop_down_button.set_item(str(status))
        self.ui.todo_task_actual_end_date.date_input_entry.set_text(
            self.ui.todo_task_actual_end_date.date_input_entry, str(actual_end_date))

        #
        self.ui.todo_task_start_date.date_input_entry.readonly = True
        self.ui.todo_task_expected_end_date.date_input_entry.readonly = True
        self.ui.todo_task_expected_end_date.date_input_entry.readonly = True
        self.ui.todo_task_title.readonly = True
        self.ui.todo_task_body.readonly = True
        self.ui.todo_task_assignees.readonly = True
        self.ui.percent_progress.drop_down_button.disabled = True


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = ViewTodoController(None, None, 1)

            return app

    MainApp().run()