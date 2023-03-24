from kivymd.app import MDApp
from controllers.home.main_home_controller import MainHomeController

import os, sys
from kivy.resources import resource_add_path, resource_find


if __name__ == "__main__":

    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    # log.debug("PythonLanguageServer, self.config: %s", self.config)
    # # Changing it to -->
    # if log.isEnabledFor(logging.DEBUG):
    #     create_string = str( self.config )
    #     log.debug("PythonLanguageServer, self.config: %s", create_string)

    class MainApp(MDApp):
        def __init__(self):
            super().__init__()
            self.title = "Peg"
            # self.icon = str(ICONS_FOLDER_PATH).replace('\\', '/') + 'app_icon.ico'
            # print(self.icon)

        def build(self):
            # return MDBoxLayout()
            homeview = MainHomeController()
            return homeview

    MainApp().run()