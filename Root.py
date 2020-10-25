from kivy.uix.screenmanager import ScreenManager
import os
from graphics import Spiral, Two_Spiral

# from android.storage import primary_external_storage_path

class Root(ScreenManager):
    pathfile = './'
    # pathfile = primary_external_storage_path()
    path = os.path.join(pathfile, 'patients')
    Spiral.path = path
    Two_Spiral.path = path
    try:
        os.makedirs(path)
    except:
        pass
