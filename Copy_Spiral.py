from kivy.uix.screenmanager import Screen
from datetime import datetime
from kivymd.uix.dialog import MDDialog
import os
from graphics import Spiral, Two_Spiral
from kivy.clock import Clock
from kivymd.toast.kivytoast.kivytoast import toast
from kivy.core.window import Window
from kivy.properties import NumericProperty

class Copy_Spiral(Screen):
    filename = str()
    event = Clock.schedule_interval
    path = str()
    width = NumericProperty(10)

    def on_enter(self, *args):
        if self.filename[0] == "L":
            self.ids.toolbar.title = self.ids.toolbar.title + ', левая рука'
        elif self.filename[0] == "R":
            self.ids.toolbar.title = self.ids.toolbar.title + ', правая рука'
        # self.ids.counter.text = 'Повторите верхнюю спираль в нижнем квадрате'
        filename1 = self.filename + datetime.now().strftime("%Y.%m.%d_%H:%M:%S") + '.csv'
        Two_Spiral.pathfile = os.path.join(Two_Spiral.folderpath, filename1)

        if os.path.exists(os.path.join(Two_Spiral.path, 'two_spiral_' +
                                                    str(Window.width) + '_' +
                                                    str(Window.height) + '.csv')) == False:
            for i in range(self.ids.spiral.frames_two_spiral):
                self.ids.spiral.generate_two_spiral(i, Two_Spiral.path)
        if self.ids.spiral.readfromfile_two_spiral() == True:
            self.ids.spiral.two_spiral(self.width)
        else:
            toast('Error')
            self.ids.spiral.readfromfile_two_spiral()

    def on_leave(self):
        self.ids.spiral.clr()
