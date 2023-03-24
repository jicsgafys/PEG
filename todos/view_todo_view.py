from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield.textfield import MDTextField

from utils.widgets import AngelaBackNextButtons, AngelaCombobox
from utils.widgets import AngelaDateWidget


class ViewTodoView(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)

        self.header = MDAnchorLayout(size_hint=(1, 0.1))
        self.body = MDRelativeLayout(size_hint=(1, 1))

        self.add_widget(self.header)
        self.add_widget(self.body)

        ##############################################
        self.top_nav = MDTopAppBar(title="View Todo", elevation=4, md_bg_color=(0.2, 0.5, 0.9, 1),
                                   left_action_items=[['arrow-left', lambda x: None]])
        self.header.add_widget(self.top_nav)
        ##############################################

        ##################################################
        self.body_content = MDBoxLayout(orientation='vertical', size_hint=(1, 1),
                                        padding=[0, 0, 0, 0])
        self.body.add_widget(self.body_content)

        self.home_bottom_layout = MDScrollView(size_hint=(1, .8))
        self.body_content.add_widget(self.home_bottom_layout)

        self.home_bottom_content = MDBoxLayout(size_hint=(1, None), orientation='vertical',
                                               spacing=30)
        self.home_bottom_layout.add_widget(self.home_bottom_content)
        self.home_bottom_content.height = 890
        self.home_bottom_content.padding = [50, 10, 50, 0]

        self.todo_task_title = MDTextField(hint_text="Task")
        self.todo_task_title.size_hint = (1, 0.1)

        self.todo_task_body = MDTextField(hint_text="Description", multiline=True)
        self.todo_task_body.size_hint = (1, 0.2)

        self.todo_task_assignees = MDTextField(hint_text="Assignees", multiline=True)
        self.todo_task_assignees.size_hint = (1, 0.2)

        self.todo_task_start_date = AngelaDateWidget()
        self.todo_task_start_date.date_input_entry.hint_text = "Start Date"
        self.todo_task_start_date.select_button.disabled = True
        self.todo_task_start_date.remove_widget(self.todo_task_start_date.clear_button)
        self.todo_task_start_date.size_hint = (1, 0.1)
        self.todo_task_start_date.height = 50

        self.todo_task_expected_end_date = AngelaDateWidget()
        self.todo_task_expected_end_date.date_input_entry.hint_text = "Expected End Date"
        self.todo_task_expected_end_date.select_button.disabled = True
        self.todo_task_expected_end_date.remove_widget(self.todo_task_expected_end_date.clear_button)
        self.todo_task_expected_end_date.size_hint = (1, 0.1)
        self.todo_task_expected_end_date.height = 50

        self.percent_progress = AngelaCombobox("Percentage Progress", [])
        self.percent_progress.drop_down_button.set_item(str(10))
        self.percent_progress.title_label.color = (0, 0, 0, 0.4)
        self.percent_progress.title_label.bold = False
        self.percent_progress.title_label.italic = False
        self.percent_progress.size_hint = (0.5, 0.1)
        self.percent_progress.height = 50

        self.todo_task_actual_end_date = AngelaDateWidget()
        self.todo_task_actual_end_date.date_input_entry.hint_text = "Actual End Date"
        self.todo_task_actual_end_date.select_button.disabled = True
        self.todo_task_actual_end_date.remove_widget(self.todo_task_actual_end_date.clear_button)
        self.todo_task_actual_end_date.size_hint = (1, 0.1)
        self.todo_task_actual_end_date.height = 50

        self.home_bottom_content.add_widget(self.todo_task_title)
        self.home_bottom_content.add_widget(self.todo_task_body)
        self.home_bottom_content.add_widget(self.todo_task_assignees)
        self.home_bottom_content.add_widget(self.todo_task_start_date)
        self.home_bottom_content.add_widget(self.todo_task_expected_end_date)
        self.home_bottom_content.add_widget(self.percent_progress)
        self.home_bottom_content.add_widget(self.todo_task_actual_end_date)

        self.action_buttons_layout = MDAnchorLayout(anchor_x="right", anchor_y="bottom",
                                                    size_hint=(1, None),)
        self.action_buttons_layout.padding = [0, 50, 0, 50]
        self.home_bottom_content.add_widget(self.action_buttons_layout)

        self.action_buttons = AngelaBackNextButtons()
        self.action_buttons.size_hint = (0.6, None)
        self.action_buttons.height = 60
        # self.action_buttons.remove_widget(self.action_buttons.back_button)  # Removes the back button
        self.action_buttons.next_button.text = "Save"  # Changes the name of the next button to 'Save'
        self.action_buttons_layout.add_widget(self.action_buttons)
        ##################################################


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            app = ViewTodoView()

            return app

    MainApp().run()