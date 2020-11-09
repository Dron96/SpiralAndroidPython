from kivymd.app import MDApp
from kivy.app import App
from kivy.base import EventLoop
from Main_Screen import Main
from Root import Root
from Copy_Spiral import Copy_Spiral
from New_Patient import New_Patient
from Bad_Habits import Bad_Habits
from Methods_Hands import Methods_Hands


# from android.permissions import request_permissions, Permission
# from android.storage import primary_external_storage_path


class Example1App(MDApp):

    def build(self):
        # request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
        return Root()

    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            app = App.get_running_app()
            if app.root.current != 'main':
                app.root.current = 'main'
            return True


Example1App().run()

__version__ = 0.1
