from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivy.app import App
import os
from graphics import Spiral, Two_Spiral
from Root import Root
from One_Spiral import One_Spiral
from Bad_Habits import Bad_Habits
import datetime


class New_Patient(Screen):
    addpath = str()
    pat_id = str()
    diagnosis = 'Здоров'
    hand = str()
    sex = str()


    def callback_sex(self, text, checkbox, value):
        if value:
            self.sex = text

    def callback_hand(self, text, checkbox, value):
        if value:
            self.hand = text


    def my_callback(self, text_of_selection, popup_widget):
        if text_of_selection == 'Отмена':
            pass
        else:
            Bad_Habits.person = self.pat_id
            Spiral.folderpath = self.addpath
            Two_Spiral.folderpath = self.addpath
            self.manager.current = 'bad_habits'

    def new_folder(self):
        try:
            datetime.datetime.strptime(str(self.ids.dob.text), "%d.%m.%Y")
            try:
                self.pat_id = str(self.ids.family_name.text) + ' ' + str(self.ids.name.text[0]) \
                              + '.' + str(self.ids.father_name.text[0]) + '. '' ' + str(self.ids.dob.text)
                self.addpath = os.path.join(Root.path, self.pat_id)

                try:
                    os.makedirs(self.addpath)
                    pathfile = os.path.join(self.addpath, 'Информация.txt')
                    with open(pathfile, 'a') as ouf:
                        ouf.write('Фамилия: ' + str(self.ids.family_name.text) + '\n')
                        ouf.write('Имя: ' + str(self.ids.name.text) + '\n')
                        ouf.write('Отчество: ' + str(self.ids.father_name.text) + '\n')
                        ouf.write('Дата рождения: ' + str(self.ids.dob.text) + '\n')
                        ouf.write('Диагноз: ' + self.diagnosis + '\n')
                        ouf.write('Пол: ' + self.sex + '\n')
                        ouf.write('Доминирующая рука: ' + self.hand + '\n')
                    MDDialog(
                        text='[size=50][color=ff3333]' + self.pat_id + '[/color], проверьте еще раз свои данные:[/size]',
                        size_hint=[.8, .4],
                        events_callback=self.my_callback, text_button_ok='Отмена', text_button_cancel='Все правильно',
                        title='').open()
                except OSError:
                    MDDialog(text='Пациент с данным id уже существует. Придумайте новый id', title='Ошибка в id',
                             size_hint=[.8, .4]).open()

            except IndexError:
                MDDialog(text='Заполните, пожалуйста, все поля', title='Пустое поле',
                         size_hint=[.8, .4]).open()

        except ValueError:
            MDDialog(text='Поле "Дата рождения" заполнено неправильно. Заполните, пожалуйста, в виде ДД.ММ.ГГГГ',
                     title='Неправильная дата',
                     size_hint=[.8, .4]).open()


    def callback_diagnos(self, *args):
        t = args[0]
        self.ids.diagnos.text = t
        self.diagnosis = t


    def diagnos_dropmenu(self):
        menu_items = []
        app = App.get_running_app()
        items = ['Здоров', 'Эссенциальный тремор', 'Болезнь Паркинсона', 'Дистония ',
                 'Рассеянный склероз', 'Гиперкинезы', 'Тиреотоксикоз (гипертиреоз)', 'Другие']
        for i in items:
            menu_items.append(
                {
                    "viewclass": "MDMenuItem",
                    "text": i,
                    "spacing": 20,
                    "width": app.root.width,
                    "font_size": 40,
                    "text_color": (1, 1, 1, 1),
                    "callback": self.callback_diagnos,
                }
            )
        MDDropdownMenu(items=menu_items, width_mult=5, border_margin=10, _center=True,
                       max_height=app.root.height / 2, ver_growth="down", pos=self.pos).open(self)

    def on_leave(self, *args):
        self.ids.family_name.text = ''
        self.ids.name.text = ''
        self.ids.father_name.text = ''
        self.ids.dob.text = ''
        self.ids.diagnos.text = 'Здоров'
        self.diagnosis = 'Здоров'
        for i in [self.ids.Men, self.ids.Women, self.ids.Right,
                  self.ids.Left, self.ids.AmbiDexter]:
            i.ids.check.active = False