from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.clock import Clock

from controllers.todos.edit_todo_controller import EditTodoController
from controllers.todos.create_new_todo_controller import CreateNewTodoController
from controllers.todos.todos_list_controller import TodosListController
from controllers.todos.view_todo_controller import ViewTodoController


class MainTodoController(MDBoxLayout):
    def __init__(self):
        super().__init__()

        # Default home screen for the page
        self.todos_list_controller = TodosListController()
        self.add_widget(self.todos_list_controller)

        # Bindings
        self.todos_list_controller.ui.new_todo_button.on_release = lambda: self.show_create_new_todo()
        self.todos_list_controller.ui.edit_todo_button.on_release = lambda: self.show_edit_todo()
        self.todos_list_controller.ui.view_todo_button.on_release = lambda: self.show_view_todo()

    def show_create_new_todo(self):
        try:
            create_new_todo_controller = CreateNewTodoController(self, self.todos_list_controller)
            Clock.schedule_once(lambda x: transition(), 0)
            self.remove_widget(self.todos_list_controller)
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.add_widget(create_new_todo_controller)
            create_new_todo_controller.size_hint_y = 0
            anim.start(create_new_todo_controller)

    def show_edit_todo(self):
        try:
            sel_todo = self.todos_list_controller.ui.todos_table.get_row_checks()  # [[], []]
            if sel_todo:
                if sel_todo[0]:
                    _todo_id = sel_todo[0][0]
                    edit_todo_controller = EditTodoController(self, self.todos_list_controller, _todo_id)
                    Clock.schedule_once(lambda x: transition(), 0)
                    self.remove_widget(self.todos_list_controller)
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.add_widget(edit_todo_controller)
            edit_todo_controller.size_hint_y = 0
            anim.start(edit_todo_controller)

    def show_view_todo(self):
        try:
            sel_todo = self.todos_list_controller.ui.todos_table.get_row_checks()  # [[], []]
            if sel_todo:
                if sel_todo[0]:
                    _todo_id = sel_todo[0][0]
                    view_todo_controller = ViewTodoController(self, self.todos_list_controller, _todo_id)
                    Clock.schedule_once(lambda x: transition(), 0)
                    self.remove_widget(self.todos_list_controller)
        except:
            pass

        def transition():
            anim = Animation(size_hint=(1, 1), duration=0.2)
            self.add_widget(view_todo_controller)
            view_todo_controller.size_hint_y = 0
            anim.start(view_todo_controller)


if __name__ == "__main__":
    from kivy.core.window import Window

    Window.size = (360, 640)


    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = MainTodoController()

            return app


    MainApp().run()
