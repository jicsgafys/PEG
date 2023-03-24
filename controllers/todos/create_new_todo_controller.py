from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker

from models.todos.todos import AddNewTodo
from views.todos.create_new_todo_view import CreateNewTodoView


class CreateNewTodoController(MDBoxLayout):
    def __init__(self, main_container_widget, previous_widget):
        super().__init__()
        self.main_container_widget = main_container_widget
        self.previous_widget = previous_widget

        self.ui = CreateNewTodoView()
        self.add_widget(self.ui)

        self.ui.todo_task_start_date.select_button.on_release = lambda: self.set_start_date_date()
        self.ui.todo_task_expected_end_date.select_button.on_release = lambda: self.set_expected_end_date_date()
        self.ui.todo_task_actual_end_date.select_button.on_release = lambda: self.set_actual_end_date_date()
        self.ui.top_nav.left_action_items[0] = ['arrow-left', lambda x: self.back_to_previous_widget()]
        self.ui.action_buttons.back_button.on_release = lambda: self.back_to_previous_widget()
        self.ui.action_buttons.next_button.on_release = lambda: self.save_todo()

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

    def save_todo(self):
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

        title = self.ui.todo_task_title.text
        description = self.ui.todo_task_body.text
        assignees = self.ui.todo_task_assignees.text
        start_date = self.ui.todo_task_start_date.date_input_entry.text
        expected_end_date = self.ui.todo_task_expected_end_date.date_input_entry.text
        status = self.ui.percent_progress.drop_down_button.current_item
        actual_end_date = self.ui.todo_task_actual_end_date.date_input_entry.text

        if str(title).strip() != "":
            dialog.open()

        def continue_save():
            note = AddNewTodo()
            note.insert(title, description, assignees, start_date, expected_end_date, status,
                        actual_end_date)
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
            app = CreateNewTodoController(None, None)

            return app

    MainApp().run()