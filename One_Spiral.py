from kivy.uix.screenmanager import Screen
from datetime import datetime
from kivymd.uix.dialog import MDDialog
import os
from graphics import Spiral
from kivy.clock import Clock
from kivymd.toast.kivytoast.kivytoast import toast
from kivy.core.window import Window
from kivy.properties import NumericProperty
from Copy_Spiral import Copy_Spiral

class One_Spiral(Screen):
    filename = str()
    event = Clock.schedule_interval
    path = str()
    width = NumericProperty(10)
    bad_habits = str()

    def on_enter(self, *args):
        if self.width == 3:
            self.ids.toolbar.title = 'Врисование'
        elif self.width == 10:
            self.ids.toolbar.title = 'Спираль'
        if self.filename[0] == "L":
            self.ids.toolbar.title = self.ids.toolbar.title + ', левая рука'
        elif self.filename[0] == "R":
            self.ids.toolbar.title = self.ids.toolbar.title + ', правая рука'
        # self.ids.counter.text = 'Проведите линию по спирали от синей до красной точки'
        filename1 = self.filename + datetime.now().strftime("%Y.%m.%d_%H:%M:%S") + '.csv'
        Spiral.pathfile = os.path.join(Spiral.folderpath, filename1)

        if os.path.exists(os.path.join(Spiral.path,
                                       str(Window.width) + '_'+
                                       str(Window.height) + '.csv')) == False:
            for i in range(self.ids.spiral.frames):
                self.ids.spiral.generate_spiral(i, Spiral.path)
        if self.ids.spiral.readfromfile() == True:
            toast (str(len(self.ids.spiral.points)))
            self.ids.spiral.static_spiral(self.width)
        else:
            toast ('Error')
            self.ids.spiral.readfromfile()


    def on_leave(self):
        if self.width == 3:
            self.ids.spiral.clr()
            Copy_Spiral.width = 7
            self.manager.current = 'copy_spiral'
            Copy_Spiral.filename = self.filename[0] + "_Cp_" + self.bad_habits + '_'
        if self.width == 10:
            self.ids.spiral.clr()
            One_Spiral.width = 3
            One_Spiral.filename = self.filename[0] + "_In_" + self.bad_habits + '_'
            self.on_enter()
            print(self.filename[0])
            print(One_Spiral.filename)

    def to_main(self):
        self.manager.current = 'main'