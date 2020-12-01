import os
import re
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from database import create_connection as create_connection
import json


def upload(df, table_name):
    con = create_engine('postgresql+psycopg2://dron:@127.0.0.1:5432/spiral')

    df.to_sql(
        table_name,
        con,
        if_exists='append',
        index=False
    )


path = '/Users/dron/PycharmProjects/Спиралька/Обработка данных/Patients_parse'
exam_ind = {'user_id': int,
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
print(path)
os.chdir(path)
print()

info = pd.DataFrame()
folders = os.listdir(path)
for folder in folders:
    if os.path.isdir(folder):
        files = os.listdir(folder)
        os.chdir(folder)
        df = pd.read_csv('Информация.txt', sep=': ', header=None, index_col=0)
        info = df.transpose()
        print(os.getcwd())
        print(info)

        files.remove('Информация.txt')
        examinations = pd.DataFrame(columns=exam_ind)
        for file in files:
            data = pd.read_csv(file, names=['t', 'x', 'y'])
            data = data.to_json(orient='columns')
            # parsed = json.loads(data)
            # print(json.dumps(parsed, indent=1))
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
            upload(info, 'users')
        except IntegrityError:
            pass
        values = info[['first_name',
                       'second_name',
                       'middle_name',
                       'diagnosis',
                       'dob']].values
        user_id_query = """
        SELECT id FROM users WHERE
        first_name = %s AND
        second_name = %s AND
        middle_name = %s AND
        diagnosis = %s AND
        dob = %s
        """
        conn = create_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(user_id_query, values.tolist()[0])
        user_id = cursor.fetchone()[0]
        examinations['user_id'] = user_id
        print(examinations)
        try:
            upload(examinations, 'examinations')
        except IntegrityError:
            pass

        os.chdir('../')
