from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.app import App
from graphics import Spiral, Two_Spiral
from Root import Root
from Bad_Habits import Bad_Habits as BH
from kivymd.uix.dialog import MDDialog
import os
import re
import pandas as pd
from sqlalchemy.exc import IntegrityError
from database import create_connection as create_connection
from kivymd.toast.kivytoast.kivytoast import toast

from upload_to_DB import upload


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

    def upload_to_db(self):
        path = Root.path
        exam_ind = {'patient_id': int,
                    'hand': str,
                    'type': str,
                    'bad_effects': str,
                    'exam_date': str,
                    'exam_time': str,
                    'data': dict
                    }
        new_names = {
            "Фамилия": 'second_name',
            "Имя": 'first_name',
            "Отчество": 'middle_name',
            "Дата рождения": 'dob',
            "Диагноз": 'diagnosis',
            "Пол": 'sex',
            "Доминирующая рука": 'dominant_hand'
        }
        os.chdir(path)

        info = pd.DataFrame()
        folders = os.listdir(path)

        toast('upload_to_db')

        for folder in folders:
            if os.path.isdir(folder):
                files = os.listdir(folder)
                os.chdir(folder)
                df = pd.read_csv('Информация.txt', sep=': ', header=None, index_col=0)
                info = df.transpose()

                files.remove('Информация.txt')
                examinations = pd.DataFrame(columns=exam_ind)
                for file in files:
                    data = pd.read_csv(file, names=['t', 'x', 'y'])
                    data = data.to_json(orient='columns')
                    exam = re.split('[_| ]', file)
                    if len(exam) == 3:
                        exam = {
                            'hand': exam[0],
                            'exam_date': exam[1],
                            'exam_time': exam[2].rstrip('.csv'),
                            'data': data
                        }
                    elif len(exam) == 5:
                        exam = {
                            'hand': exam[0],
                            'type': exam[1],
                            'bad_effects': exam[2],
                            'exam_date': exam[3],
                            'exam_time': exam[4].rstrip('.csv'),
                            'data': data
                        }
                    exam = pd.DataFrame([exam], columns=exam.keys())
                    examinations = pd.concat([examinations, exam])

                info['Дата рождения'] = pd.to_datetime(info['Дата рождения'])
                info.rename(new_names, axis=1)
                try:
                    info.loc[info['Пол'] == 'Мужской', 'Пол'] = True
                    info.loc[info['Пол'] == 'Женский', 'Пол'] = False
                except KeyError:
                    pass
                try:
                    info.loc[info['Доминирующая рука'] == 'Левая', 'Доминирующая рука'] = 'L'
                    info.loc[info['Доминирующая рука'] == 'Правая', 'Доминирующая рука'] = 'R'
                    info.loc[info['Доминирующая рука'] == 'Обе', 'Доминирующая рука'] = 'B'
                except KeyError:
                    pass
                try:
                    info = info.rename(new_names, axis=1)
                    print('nen', info)
                    upload(info, 'patients')
                except IntegrityError:
                    pass
                values = info[['first_name',
                               'second_name',
                               'middle_name',
                               'diagnosis',
                               'dob']].values
                patient_id_query = """
                SELECT id FROM patients WHERE
                first_name = %s AND
                second_name = %s AND
                middle_name = %s AND
                diagnosis = %s AND
                dob = %s
                """
                conn = create_connection()
                conn.autocommit = True
                cursor = conn.cursor()
                cursor.execute(patient_id_query, values.tolist()[0])
                patient_id = cursor.fetchone()[0]
                examinations['patient_id'] = patient_id
                try:
                    upload(examinations, 'examinations')
                except IntegrityError:
                    pass

                os.chdir('../')