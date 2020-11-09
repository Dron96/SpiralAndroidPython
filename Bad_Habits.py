from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast.kivytoast import toast
import time
from kivymd.uix.dialog import MDDialog
from One_Spiral import One_Spiral
from Copy_Spiral import Copy_Spiral


class Bad_Habits(Screen):
    bad_habits = {}
    person = str()
    person_habits = []
    answer = False
    hand = str()
    checkbox_group = {'C': 'C',
                      "E": 'E',
                      "S": 'S',
                      "A": 'A',
                      'M': 'M',
                      'F': 'F',
                      'N': 'N'}
    person_habits_str = str()

    def on_enter(self, *args):
        self.answer = False
        self.person_habits = []
        if self.person in self.bad_habits.keys():
            self.answer = True
            if (time.time() - self.bad_habits[self.person][0]) <= 30*60:
                if self.bad_habits[self.person][1] != "":
                    MDDialog(text='[size=50]Выберите руку, которой будете рисовать:[/size]',
                             title='Выбор руки',
                             events_callback=self.my_callback,
                             text_button_ok='[size=50]Левая рука[/size]',
                             text_button_cancel='[size=50]Правая рука[/size]',
                             size_hint=[.8, .4]).open()
            else:
                self.answer = False

    def bad_habits_to_str(self, *args):
        self.person_habits_str = ''
        if self.answer == False:
            for i in self.person_habits:
                self.person_habits_str += i
                if i == "N" and len(self.person_habits) != 1:
                    self.person_habits_str = ''
                    break
            self.bad_habits[self.person] = [time.time(), self.person_habits_str]
            for i in [self.ids.Coffee, self.ids.Energetic, self.ids.Alcohol,
                      self.ids.Medicine, self.ids.Smoke, self.ids.PhisicalExercise,
                      self.ids.Nothing]:
                i.ids.check.active = False


    def callback(self, text, checkbox, value):
        toast(checkbox.group)
        if value:
            self.person_habits.append(checkbox.group)
        else:
            if checkbox.group in self.person_habits:
                self.person_habits.remove(checkbox.group)

    def confirm(self):
        self.bad_habits_to_str()
        if self.person_habits_str == '':
            MDDialog(text='[size=50]Выберите хотя бы один пункт.[/size]',
                     title='Неправильное заполнение',
                     size_hint=[.8, .4]).open()
        else:
            MDDialog(text='[size=50]Выберите руку, которой будете рисовать:[/size]',
                     title='Выбор руки',
                     events_callback=self.my_callback,
                     text_button_ok='[size=50]Левая рука[/size]',
                     text_button_cancel='[size=50]Правая рука[/size]',
                     size_hint=[.8, .4]).open()

    def my_callback(self, text_of_selection, popup_widget):
        if text_of_selection == 'Левая':
            self.hand = 'L'
        else:
            self.hand = 'R'
        One_Spiral.width = 10
        self.manager.current = 'one_spiral'
        One_Spiral.bad_habits = self.person_habits_str
        Copy_Spiral.bad_habits = self.person_habits_str
        One_Spiral.filename = self.hand + "_Sp_" + self.person_habits_str + '_'