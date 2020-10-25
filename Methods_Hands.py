from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from One_Spiral import One_Spiral
from Copy_Spiral import Copy_Spiral
from Bad_Habits import Bad_Habits


class Methods_Hands(Screen):
    method = str()
    hand = str()
    person = str
    methods = {'Спираль':'Sp',
               'Врисование': 'In',
               'Копия': 'Cp'}
    hands = {'Левая': 'L',
             'Правая': 'R'}
    bh = str()

    def on_leave(self, *args):
        for i in [self.ids.Spiral, self.ids.Copy, self.ids.InDraw,
                  self.ids.Left, self.ids.Right]:
            i.ids.check.active = False
        method = str()
        hand = str()


    def callback_methods(self,text, checkbox, value):
        if value:
            self.method = text
        else:
            if (text == self.method) or (text in self.methods.keys()):
                self.method = ''

    def callback_hands(self, text, checkbox, value):
        if value:
            self.hand = text
        else:
            if (text == self.hand) or (text in self.hands.keys()):
                self.hand = ''

    def confirm(self):
        if self.method == '' or self.hand == '':
            MDDialog(text='Заполните, пожалуйста, все поля', title='Пустое поле',
                     size_hint=[.8, .4]).open()
        else:
            if self.method not in self.methods.values():
                self.method = self.methods[self.method]
            if self.hand not in self.hands.values():
                self.hand = self.hands[self.hand]
            self.selected_method()
        self.bad_habits()

    def selected_method(self):
        if self.method == 'Sp':
            One_Spiral.width = 10
            self.manager.current = 'one_spiral'
            One_Spiral.filename = self.hand + "_" + self.method + "_" + self.bad_habits() + '_'
        elif self.method == 'Cp':
            Copy_Spiral.width = 7
            self.manager.current = 'copy_spiral'
            Copy_Spiral.filename = self.hand + "_" + self.method + "_" + self.bad_habits() + '_'
        elif self.method == 'In':
            One_Spiral.width = 3
            self.manager.current = 'one_spiral'
            One_Spiral.filename = self.hand + "_" + self.method + "_" + self.bad_habits() + '_'

    def bad_habits(self):
        BH = Bad_Habits.bad_habits[Bad_Habits.person][1]
        if BH == '':
            BH = 'N'
        return BH
