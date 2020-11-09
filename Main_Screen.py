from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.app import App
import os
from graphics import Spiral, Two_Spiral
from Root import Root
from One_Spiral import One_Spiral
from Bad_Habits import Bad_Habits as BH
from kivymd.uix.dialog import MDDialog


class Main(Screen):

    def my_callback(self, text_of_selection, popup_widget):
        if text_of_selection == 'Отмена':
            pass
        else:
            addpath = os.path.join(Root.path, BH.person)
            Spiral.folderpath = addpath
            Two_Spiral.folderpath = addpath
            self.manager.current = 'bad_habits'

    def callback_for_menu_items(self, *args):
        t = args[0]
        BH.person = str(t)
        MDDialog(
            text='[size=40][color=ff3333]' + t + '[/color], хотите продолжить?[/size]',
            size_hint=[.8, .4],
            events_callback=self.my_callback, text_button_ok='Отмена', text_button_cancel='Продолжить',
            title='').open()

    def build(self):
        app = App.get_running_app()
        dirs = []
        menu_items = []
        for dirname, dirnames, filenames in os.walk(Root.path):
            dirs.append(dirnames)
        if len(dirs) >= 1:
            items = dirs[0]
            for i in range(len(items)):
                menu_items.append(
                    {
                        "viewclass": "MDMenuItem",
                        "text": items[i],
                        "spacing": 20,
                        "width": app.root.width,
                        "font_size": 40,
                        "text_color": (1, 1, 1, 1),
                        "callback": self.callback_for_menu_items,
                    }
                )
            MDDropdownMenu(items=menu_items, width_mult=5, border_margin=10, _center=True,
                           max_height=app.root.height / 2, ver_growth="down", pos=self.pos).open(self)
