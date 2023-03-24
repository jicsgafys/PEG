from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.card.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
# from kivymd.uix.carousel import MDCarousel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label.label import MDLabel
# from kivymd.uix.fitimage.fitimage import FitImage
from kivy.uix.image import Image
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu.menu import MDDropdownMenu
from kivymd.uix.dropdownitem.dropdownitem import MDDropDownItem
# from kivymd.uix.list.list import OneLineListItem
from kivy.metrics import dp

from utils.paths import ICONS_FOLDER_PATH, DISK_ROOT_PATH


class AngelaCard(MDCard):
    def __init__(self, imagepath, text):
        super().__init__()
        self.size_hint = (1, 1)

        self.cover = MDBoxLayout(orientation='vertical', size_hint=(1, 1),
                                 radius=10, line_width=1, line_color=(0, 0, 0, 0.2), padding=2)
        self.add_widget(self.cover)

        self.cover_sub1 = MDBoxLayout(orientation='vertical', size_hint=(1, 1))
        self.cover_sub2 = MDAnchorLayout(size_hint=(1, 0.2), anchor_y='top')

        self.cover.add_widget(self.cover_sub1)
        self.cover.add_widget(self.cover_sub2)

        self.image = Image(size_hint=(1, 1), source=imagepath)
        self.cover_sub1.add_widget(self.image)

        self.label = MDLabel(text=text, halign='center', font_style="H6",
                             font_name='Arial')
        self.cover_sub2.add_widget(self.label)


class AngelaFileUpload(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'horizontal'
        self.padding = 10
        self.spacing = 10

        self.upload_input_entry = MDTextField(readonly=True, size_hint=(0.8, 1), hint_text="Upload File")
        self.upload_button = MDIconButton(text='Choose', size_hint=(None, None), icon='upload')
        self.clear_button = MDIconButton(text='Clear', size_hint=(None, None), icon='close')

        self.add_widget(self.upload_input_entry)
        self.add_widget(self.upload_button)
        self.add_widget(self.clear_button)


class AngelaCheckbox(MDBoxLayout):
    def __init__(self, text):
        super().__init__()
        self.orientation = 'horizontal'

        self.checkbox = MDCheckbox(size_hint=(.2, 1))
        self.checkbox_title = MDLabel(text=str(text), size_hint=(.8, 1))

        self.add_widget(self.checkbox)
        self.add_widget(self.checkbox_title)


class AngelaBackNextButtons(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'horizontal'
        self.padding = 10
        self.spacing = 30

        self.back_button = MDRectangleFlatButton(text='Back', size_hint=(0.5, 1), font_style="Subtitle1",
                                                 line_color=(0.2, 0.5, 0.9, 1))
        self.next_button = MDRectangleFlatButton(text='Next', size_hint=(0.5, 1), font_style="Subtitle1",
                                                 line_color=(0.2, 0.5, 0.9, 1))

        self.add_widget(self.back_button)
        self.add_widget(self.next_button)


class AngelaCombobox(MDBoxLayout):
    def __init__(self, title, menu_items_list):
        super().__init__()
        self.orientation = 'vertical'

        self.title_label = MDLabel(text=str(title), font_style="Subtitle1", size_hint=(1, 0.3), italic=True,
                                   bold=True)
        self.drop_down_button = MDDropDownItem(size_hint=(1, 0.7))
        self.drop_down_button.set_item("Select Column")
        self.drop_down_button.on_release = lambda: self.drop_down_menu.open()

        self.add_widget(self.title_label)
        self.add_widget(self.drop_down_button)

        self.menu_items = []
        for item in menu_items_list:
            item_widget = {
                'viewclass': "OneLineListItem",
                'text': str(item),
                "height": dp(56),
                'on_release': lambda x=str(item): self.set_item(x)
            }
            self.menu_items.append(item_widget)

        self.drop_down_menu = MDDropdownMenu(caller=self.drop_down_button, width_mult=4,
                                             items=self.menu_items, position='center')
        self.drop_down_menu.radius = [0, 20, 0, 20]
        self.drop_down_menu.bind()

    def set_item(self, text_item):
        self.drop_down_button.set_item(text_item)
        self.drop_down_menu.dismiss()


class AngelaLabeledTwoEntrybox(MDBoxLayout):
    def __init__(self, title):
        super().__init__()
        self.orientation = 'vertical'

        self.sub1 = MDBoxLayout(orientation='vertical', size_hint=(1, 0.3))
        self.sub2 = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.7))
        self.sub2.spacing = 20

        self.add_widget(self.sub1)
        self.add_widget(self.sub2)

        self.title_label = MDLabel(text=str(title), font_style="Subtitle1", size_hint=(1, 1), italic=True,
                                   bold=True)
        self.sub1.add_widget(self.title_label)

        self.first_entry = MDTextField(hint_text="K Value", size_hint=(0.5, 1))
        self.second_entry = MDTextField(hint_text="S Value", size_hint=(0.5, 1))
        self.sub2.add_widget(self.first_entry)
        self.sub2.add_widget(self.second_entry)


class AngelaDateWidget(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'horizontal'
        # self.padding = 10
        self.spacing = 10

        self.date_input_entry = MDTextField(readonly=True, size_hint=(0.8, 1), hint_text="Date")
        self.select_button = MDIconButton(text='Pick', size_hint=(None, None), icon='calendar')
        self.clear_button = MDIconButton(text='Clear', size_hint=(None, None), icon='close')

        self.add_widget(self.date_input_entry)
        self.add_widget(self.select_button)
        self.add_widget(self.clear_button)


class AngelaSearchWidget(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'horizontal'
        # self.padding = 10
        self.spacing = 10

        self.search_input_entry = MDTextField(size_hint=(0.8, 1), hint_text="Search")
        self.search_button = MDIconButton(text='Pick', size_hint=(None, None), icon='magnify')
        self.refresh_button = MDIconButton(icon=ICONS_FOLDER_PATH + 'refresh.png', size_hint=(None, None))
        # self.refresh_button.size = (8, 5)

        self.add_widget(self.search_input_entry)
        self.add_widget(self.search_button)
        self.add_widget(self.refresh_button)


class AngelaConfirmationDialog:
    def __init__(self, title, text):
        self.no_btn = MDFlatButton(text="No")
        self.yes_btn = MDFlatButton(text="Yes")

        self.no_btn.on_release = lambda: self.dialog.dismiss()

        self.dialog = MDDialog(
            title=str(title),
            text=str(text),
            buttons=[
                self.no_btn, self.yes_btn
            ]
        )


class AngelaStatusDialog:
    def __init__(self, title, text):
        self.cancel_btn = MDFlatButton(text="Cancel")
        self.okay_btn = MDFlatButton(text="Ok")
        self.cancel_btn.on_release = lambda: self.dialog.dismiss()

        self.dialog = MDDialog(
            title=str(title),
            text=str(text),
            buttons=[
                self.cancel_btn, self.okay_btn,
            ]
        )

        # self.dialog.buttons[-1].on_release = lambda: self.dialog.dismiss()


class AngelaSingleTextInputDialog:
    def __init__(self, title, input_box_hint):
        self.dialog_content = AngelaLabeledTwoEntrybox("")
        self.dialog_content.size_hint_y = None
        self.dialog_content.height = 50
        self.dialog_content.sub1.remove_widget(self.dialog_content.title_label)
        self.dialog_content.sub2.remove_widget(self.dialog_content.second_entry)
        self.dialog_content.first_entry.hint_text = str(input_box_hint)

        self.cancel_btn = MDFlatButton(text="Cancel")
        self.cancel_btn.on_release = lambda: self.dialog.dismiss()
        self.ok_btn = MDFlatButton(text="Ok")

        self.dialog = MDDialog(
            title=str(title),
            type='custom',
            content_cls=self.dialog_content,
            buttons=[
                self.cancel_btn, self.ok_btn
            ]
        )

        # self.dialog.open()


# class AngelaPopupFileManager:
#     def __init__(self, title):
#         self.file_manager = MDFileManager(
#             exit_manager=self.exit_manager,
#             select_path=self.select_path,
#             selector='file',
#             ext=['.csv', ]
#         )
#         self.file_manager.size_hint = (.5, .5)
#         # self.file_manager.height = 100
#
#         self.cancel_btn = MDFlatButton(text="Cancel")
#         self.cancel_btn.on_release = lambda: self.dialog.dismiss()
#         self.ok_btn = MDFlatButton(text="Ok")
#
#         self.dialog = MDDialog(
#             title=str(title),
#             type='custom',
#             # content_cls=self.file_manager,
#             buttons=[
#                 self.cancel_btn, self.ok_btn
#             ]
#         )
#         # self.file_manager.parent = self.dialog
#         self.dialog.open()
#         self.open_file_manager()
#
#     def open_file_manager(self):
#         self.file_manager.show(DISK_ROOT_PATH)
#
#     def exit_manager(self, *args):
#         self.file_manager.close()
#
#     def select_path(self, path):
#         self.exit_manager()


class AngelaPopupFileManager:
    def __init__(self, selector):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            selector=str(selector),  # ['any', 'file', 'folder', 'multi']
            ext=['.csv', ]
        )
        self.file_manager.size_hint = (1, .8)
        # self.open_file_manager()
        # self.file_manager.select_path = lambda x: print(x)

    def open_file_manager(self):
        self.file_manager.show(DISK_ROOT_PATH)

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.exit_manager()


if __name__ == "__main__":
    class MainApp(MDApp):
        def __init__(self):
            super().__init__()

        def build(self):
            # home_carousel1 = MDCarousel(size_hint=(1, 0.5))
            # card1 = AngelaCard(IMAGES_FOLDER_PATH + "tripod.jpeg", "Image1")
            # card2 = AngelaCard(IMAGES_FOLDER_PATH + "tripod.jpeg", "Image2")
            # card3 = AngelaCard(IMAGES_FOLDER_PATH + "tripod.jpeg", "Image3")
            # home_carousel1.add_widget(card1)
            # home_carousel1.add_widget(card2)
            # home_carousel1.add_widget(card3)
            # return home_carousel1

            # fileupload = AngelaFileUpload()
            # fileupload.size_hint = (0.2, 0.2)
            # return fileupload

            # checkbox = AngelaCheckbox()
            # return checkbox

            # buttons = AngelaBackNextButtons()
            # return buttons

            # dropdown = AngelaCombobox("Backsight", ["Col" + str(x) for x in range(50)])
            # dropdown.size_hint = (0.4, 0.1)
            # return dropdown

            # doubleentry = AngelaLabeledTwoEntrybox("Misclose")
            # return doubleentry

            # search = AngelaSearchWidget()
            # return search
            layout = MDBoxLayout()
            # dialog = AngelaSingleTextInputDialog("Output Filename", 'filename')
            # dialog = AngelaPopupFileManager("folder")
            dialog = AngelaStatusDialog("folder", "")
            dialog.dialog.open()
            return layout


    MainApp().run()
