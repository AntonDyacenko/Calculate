import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidgetItem
import math
import sqlite3
import datetime
import pymorphy2
import Graph

morph = pymorphy2.MorphAnalyzer()


class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Формы/main1(1).ui', self)
        con = sqlite3.connect("База_данных/ZZZ.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Jornal
                            number""").fetchall()
        journal_list = []
        for elem in result:
            ff = []
            for i in elem:
                ff.append(i)
            journal_list.append('{0}\n{1}{2}\n'.format(ff[0], ff[1], ff[2]))
        con.close()

        self.pushButton_29.clicked.connect(self.gr)
        self.pushButton_20.clicked.connect(self.num_btn_clicked)
        self.pushButton_19.clicked.connect(self.num_btn_clicked)
        self.pushButton_18.clicked.connect(self.num_btn_clicked)
        self.pushButton_17.clicked.connect(self.num_btn_clicked)
        self.pushButton_16.clicked.connect(self.num_btn_clicked)
        self.pushButton_15.clicked.connect(self.num_btn_clicked)
        self.pushButton_14.clicked.connect(self.num_btn_clicked)
        self.pushButton_11.clicked.connect(self.num_btn_clicked)
        self.pushButton_21.clicked.connect(self.num_btn_clicked)
        self.pushButton_12.clicked.connect(self.num_btn_clicked)
        self.pushButton_10.clicked.connect(self.point)
        self.pushButton_2.clicked.connect(self.backspace)
        self.pushButton_4.clicked.connect(self.bool)
        self.pushButton.clicked.connect(self.share)
        self.pushButton_22.clicked.connect(self.equality)
        self.pushButton_3.clicked.connect(self.multiply)
        self.pushButton_9.clicked.connect(self.add)
        self.pushButton_13.clicked.connect(self.subtract)
        self.pushButton_5.clicked.connect(self.cube)
        self.pushButton_6.clicked.connect(self.square)
        self.pushButton_26.clicked.connect(self.root)
        self.pushButton_24.clicked.connect(self.arcsin)
        self.pushButton_7.clicked.connect(self.sin)
        self.pushButton_23.clicked.connect(self.arcos)
        self.pushButton_8.clicked.connect(self.cos)
        self.pushButton_25.clicked.connect(self.tg)
        self.pushButton_27.clicked.connect(self.arctg)
        self.pushButton_28.clicked.connect(self.open_second_form)
        self.listWidget.itemClicked.connect(self.connect_to_journal)
        for i in journal_list:
            self.listWidget.addItem(QListWidgetItem(str(i)))
        self.input_data = []  # список с числфми введёнными с клавиатуры
        self.action = []  # записывается действие введённое с клавиатуры
        self.copy_input_data = 0  # записывается число из 1 ввода, например записали число 4, умножили на 5,
        #  полсе ввода действия, в данном случае умножения, список str1 обнуляется, а число 4 записывается в copy_str1
        self.a3 = False  # флаг выполняемого действия, если с клавиатуры уже введено действие, флаг True

    def connect_to_journal(self, item):  # при нажатие на строку в журнале
        self.input_data = []
        aa = item.text().split('\n')[-2].split(' = ')[0]
        self.lcdNumber.display(item.text().split('\n')[-2].split(' = ')[0])
        for i in aa:
            self.input_data.append(i)

    def num_btn_clicked(self):
        if len(self.input_data) <= 15:
            if self.a3:
                self.input_data = []
                self.a3 = False
            if self.sender().text() != '0':
                self.input_data.append(self.sender().text())
                self.lcdNumber.display(float(''.join(self.input_data)))
            else:
                if self.a3:
                    self.input_data = []
                    self.a3 = False
                if ''.join(self.input_data) != '0':
                    self.input_data.append('0')
                    if self.input_data[-1] == '0' or self.input_data[-1] == '.':
                        self.lcdNumber.display(''.join(self.input_data))
                    else:
                        self.lcdNumber.display(float(''.join(self.input_data)))

    def point(self):
        if len(self.input_data) <= 14:
            if self.a3:
                self.input_data = []
                self.a3 = False
            if '.' not in self.input_data:
                self.input_data.append('.')
                self.lcdNumber.display(''.join(self.input_data))
            elif not self.input_data:
                self.input_data.append('0')
                self.input_data.append('.')
                self.lcdNumber.display(''.join(self.input_data))
            elif self.input_data[0] == '0' and self.input_data[1] != '.':
                del self.input_data[0]
                self.lcdNumber.display(''.join(self.input_data))

    def backspace(self):
        aa = 0
        for i in self.input_data:
            if i != '0' and i != '.':
                aa = 1
        if aa == 0:
            self.input_data = ['0']
            self.lcdNumber.display(''.join(self.input_data))
        if len(self.input_data) == 1:
            self.input_data = ['0']
            self.lcdNumber.display(''.join(self.input_data))
        else:
            del self.input_data[-1]
            self.lcdNumber.display(''.join(self.input_data))

    def bool(self):
        self.input_data = []
        self.action = []
        self.lcdNumber.display(float(0))

    def equality(self):
        self.today = datetime.datetime.today()
        self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
        if len(self.input_data) != 0 and self.copy_input_data != 0:
            if bool(self.copy_input_data) != 0 and self.action[0] == '/':  # если действие /
                if float(''.join(self.input_data)) != 0:
                    self.lcdNumber.display(
                        float(self.copy_input_data / float(''.join(self.input_data))))  # выводит на дисплэй
                    self.listWidget.addItem(
                        QListWidgetItem(
                            self.date + '\n' + str(
                                float(self.copy_input_data / float(''.join(self.input_data)))) + ' = ' + str(
                                self.copy_input_data) + ' / ' + str(float(''.join(self.input_data))) + '\n'))
                    self.append_in_journal(
                        self.date + '\n' + str(
                            float(self.copy_input_data / float(''.join(self.input_data)))) + ' = ' + str(
                            self.copy_input_data) + ' / ' + str(float(''.join(self.input_data))) + '\n')
                    # добавляет в журнал время и ответ
                    cc = self.input_data
                    self.input_data = []
                    self.input_data.append(str(float(self.copy_input_data / float(''.join(cc)))))
                    print(self.input_data)
                    self.action = []
                    self.copy_input_data = 0
                else:
                    self.lcdNumber.display('ERROR')
            elif bool(self.copy_input_data) != 0 and self.action[0] == '*':  # если действие *
                self.lcdNumber.display(
                    float(self.copy_input_data * float(''.join(self.input_data))))  # выводит на дисплэй
                self.listWidget.addItem(
                    QListWidgetItem(
                        self.date + '\n' + str(
                            float(self.copy_input_data * float(''.join(self.input_data)))) + ' = ' + str(
                            self.copy_input_data) + ' * ' + str(float(''.join(self.input_data))) + '\n'))
                self.append_in_journal(
                    self.date + '\n' + str(float(self.copy_input_data * float(''.join(self.input_data)))) + ' = ' + str(
                        self.copy_input_data) + ' * ' + str(float(''.join(self.input_data))) + '\n')
                # добавляет в журнал время и ответ
                cc = self.input_data
                self.input_data = []
                self.input_data.append(str(float(self.copy_input_data * float(''.join(cc)))))
                self.action = []
                self.copy_input_data = 0
            elif bool(self.copy_input_data) != 0 and self.action[0] == '+':  # если действие +
                self.lcdNumber.display(float(self.copy_input_data + float(''.join(self.input_data))))
                self.listWidget.addItem(
                    QListWidgetItem(
                        self.date + '\n' + str(
                            float(self.copy_input_data + float(''.join(self.input_data)))) + ' = ' + str(
                            self.copy_input_data) + ' + ' + str(float(''.join(self.input_data))) + '\n'))
                self.append_in_journal(
                    self.date + '\n' + str(float(self.copy_input_data + float(''.join(self.input_data)))) + ' = ' + str(
                        self.copy_input_data) + ' + ' + str(float(''.join(self.input_data))) + '\n')

                # добавляет в журнал время и ответ
                cc = self.input_data
                self.input_data = []
                self.input_data.append(str(float(self.copy_input_data + float(''.join(cc)))))
                self.action = []
                self.copy_input_data = 0
            elif bool(self.copy_input_data) != 0 and self.action[0] == '-':  # если действие -
                self.lcdNumber.display(
                    float(self.copy_input_data - float(''.join(self.input_data))))  # выводит на дисплэй
                self.listWidget.addItem(
                    QListWidgetItem(
                        self.date + '\n' + str(
                            float(self.copy_input_data - float(''.join(self.input_data)))) + ' = ' + str(
                            self.copy_input_data) + ' - ' + str(float(''.join(self.input_data))) + '\n'))
                self.append_in_journal(
                    self.date + '\n' + str(float(self.copy_input_data - float(''.join(self.input_data)))) + ' = ' + str(
                        self.copy_input_data) + ' - ' + str(float(''.join(self.input_data))) + '\n')

                # добавляет в журнал время и ответ
                cc = self.input_data
                self.input_data = []
                self.input_data.append(str(float(self.copy_input_data - float(''.join(cc)))))
                self.action = []
                self.copy_input_data = 0
            self.a3 = True

    def share(self):
        if len(self.action) == 0 and len(self.input_data) != 0:
            self.action.append('/')
            self.copy_input_data = float(''.join(self.input_data))
            self.input_data = []

    def multiply(self):
        if len(self.action) == 0 and len(self.input_data) != 0:
            self.action.append('*')
            self.copy_input_data = float(''.join(self.input_data))
            self.input_data = []

    def add(self):
        if len(self.action) == 0 and len(self.input_data) != 0:
            self.action.append('+')
            self.copy_input_data = float(''.join(self.input_data))
            self.input_data = []

    def subtract(self):
        if len(self.action) == 0 and len(self.input_data) != 0:
            self.action.append('-')
            self.copy_input_data = float(''.join(self.input_data))
            self.input_data = []

    def cube(self):
        if len(self.input_data) != 0:
            aa = float(''.join(self.input_data)) ** 3
            self.today = datetime.datetime.today()
            self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
            self.listWidget.addItem(
                QListWidgetItem(
                    self.date + '\n' + str(aa) + ' = ' + str(float(''.join(self.input_data))) + '^3' + '\n'))
            self.input_data = []
            self.input_data.append(str(aa))
            self.lcdNumber.display(float(''.join(self.input_data)))
            self.a3 = True

    def square(self):
        if len(self.input_data) != 0:
            aa = float(''.join(self.input_data)) ** 2
            self.today = datetime.datetime.today()
            self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
            self.listWidget.addItem(
                QListWidgetItem(
                    self.date + '\n' + str(aa) + ' = ' + str(float(''.join(self.input_data))) + '^2' + '\n'))
            self.input_data = []
            self.input_data.append(str(aa))
            self.lcdNumber.display(float(''.join(self.input_data)))
            self.a3 = True

    def root(self):
        if len(self.input_data) != 0:
            if float(''.join(self.input_data)) >= 0:
                aa = math.sqrt(float(''.join(self.input_data)))
                self.today = datetime.datetime.today()
                self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
                self.listWidget.addItem(
                    QListWidgetItem(
                        self.date + '\n' + str(aa) + ' = ' + '√' + str(float(''.join(self.input_data))) + '\n'))
                self.input_data = []
                self.input_data.append(str(aa))
                self.lcdNumber.display(float(''.join(self.input_data)))
                self.a3 = True
                self.a3 = True
            else:
                self.lcdNumber.display('ERROR')

    def arcsin(self):
        if len(self.input_data) != 0:
            if -1 <= float(''.join(self.input_data)) <= 1:
                aa = math.asin(float(''.join(self.input_data))) * 180 / math.pi
                self.today = datetime.datetime.today()
                self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
                self.listWidget.addItem(
                    QListWidgetItem(
                        self.date + '\n' + str(aa) + ' = ' + 'arcsin' + str(float(''.join(self.input_data))) + '\n'))
                self.input_data = []
                self.input_data.append(str(aa))
                self.lcdNumber.display(float(''.join(self.input_data)))
                self.a3 = True
            else:
                self.lcdNumber.display('ERROR')

    def sin(self):
        if len(self.input_data) != 0:
            aa = math.sin(math.radians(float(''.join(self.input_data))))
            self.today = datetime.datetime.today()
            self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
            self.listWidget.addItem(
                QListWidgetItem(
                    self.date + '\n' + str(aa) + ' = ' + 'sin' + str(float(''.join(self.input_data))) + '\n'))
            self.input_data = []
            self.input_data.append(str(aa))
            self.lcdNumber.display(float(''.join(self.input_data)))
            self.a3 = True

    def cos(self):
        if len(self.input_data) != 0:
            aa = math.cos(math.radians(float(''.join(self.input_data))))
            self.today = datetime.datetime.today()
            self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
            self.listWidget.addItem(
                QListWidgetItem(
                    self.date + '\n' + str(aa) + ' = ' + 'cos' + str(float(''.join(self.input_data))) + '\n'))
            self.input_data = []
            self.input_data.append(str(aa))
            self.lcdNumber.display(float(''.join(self.input_data)))
            self.a3 = True

    def arcos(self):
        if len(self.input_data) != 0:
            if -1 <= float(''.join(self.input_data)) <= 1:
                aa = math.acos(float(''.join(self.input_data))) * 180 / math.pi
                self.today = datetime.datetime.today()
                self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
                self.listWidget.addItem(
                    QListWidgetItem(
                        self.date + '\n' + str(aa) + ' = ' + 'arcos' + str(float(''.join(self.input_data))) + '\n'))
                self.input_data = []
                self.input_data.append(str(aa))
                self.lcdNumber.display(float(''.join(self.input_data)))
                self.a3 = True
            else:
                self.lcdNumber.display('ERROR')

    def tg(self):
        if len(self.input_data) != 0:
            aa = math.tan(math.radians(float(''.join(self.input_data))))
            self.today = datetime.datetime.today()
            self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
            self.listWidget.addItem(
                QListWidgetItem(
                    self.date + '\n' + str(aa) + ' = ' + 'tg' + str(float(''.join(self.input_data))) + '\n'))
            self.input_data = []
            self.input_data.append(str(aa))
            self.lcdNumber.display(float(''.join(self.input_data)))
            self.a3 = True

    def arctg(self):
        if len(self.input_data) != 0:
            aa = math.atan(float(''.join(self.input_data))) * 180 / math.pi
            self.today = datetime.datetime.today()
            self.date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # заполняет время
            self.listWidget.addItem(
                QListWidgetItem(
                    self.date + '\n' + str(aa) + ' = ' + 'arctg' + str(float(''.join(self.input_data))) + '\n'))
            self.input_data = []
            self.input_data.append(str(aa))
            self.lcdNumber.display(float(''.join(self.input_data)))
            self.a3 = True

    def open_second_form(self):
        self.second_form = SecondForm()
        self.second_form.show()
        self.close()

    def gr(self):
        self.a = Graph.Window()
        self.a.show()
        self.close()

    def append_in_journal(self, element):
        Date = element.split('\n')[0]
        data = float(element.split('\n')[1].split(' = ')[0])
        action = element.split('\n')[1].split(' = ')[1]
        with sqlite3.connect("База_данных/ZZZ.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Jornal(Date, data, action) VALUES('{}', '{}', ' = {}')".format(str(Date), float(data),
                                                                                            str(action)))
            con.commit()


class SecondForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Формы/Convert.ui', self)
        con = sqlite3.connect("База_данных/ZZZ.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Jornal
                                    number""").fetchall()
        journal_list = []
        for elem in result:
            ff = []
            for i in elem:
                ff.append(i)
            journal_list.append('{0}\n{1}{2}\n'.format(ff[0], ff[1], ff[2]))
        con.close()
        for i in journal_list:
            self.listWidget.addItem(QListWidgetItem(str(i)))
        # словари с константами для перевода
        self.Data_length = {
            'метры': {'миллиметры': 1000, 'сантиметры': 100, 'дециметры': 10, 'метры': 1, 'километры': 0.001},
            'миллиметры': {'миллиметры': 1, 'сантиметры': 0.1, 'дециметры': 0.01, 'метры': 0.001,
                           'километры': 0.000001},
            'сантиметры': {'миллиметры': 10, 'сантиметры': 1, 'дециметры': 0.1, 'метры': 0.01, 'километры': 0.00001},
            'дециметры': {'миллиметры': 100, 'сантиметры': 10, 'дециметры': 1, 'метры': 0.1, 'километры': 0.0001},
            'километры': {'миллиметры': 1000000, 'сантиметры': 100000, 'дециметры': 10000, 'метры': 1000,
                          'километры': 1}}
        self.Data_volume = {
            'метры': {'миллиметры': 1000 ** 3, 'сантиметры': 100 ** 3, 'дециметры': 10 ** 3, 'метры': 1, 'литры': 1000},
            'миллиметры': {'миллиметры': 1, 'сантиметры': 0.1 ** 3, 'дециметры': 0.01 ** 3, 'метры': 0.001 ** 3,
                           'литры': 0.000001},
            'сантиметры': {'миллиметры': 10 ** 3, 'сантиметры': 1, 'дециметры': 0.1 ** 3, 'метры': 0.01 ** 3,
                           'литры': 0.001},
            'дециметры': {'миллиметры': 100 ** 3, 'сантиметры': 10 ** 3, 'дециметры': 1, 'метры': 0.1 ** 3, 'литры': 1},
            'литры': {'миллиметры': 100 ** 3, 'сантиметры': 10 ** 3, 'дециметры': 1, 'метры': 0.1 ** 3, 'литры': 1}}
        self.Data_square = {
            'метры': {'миллиметры': 1000 ** 2, 'сантиметры': 100 ** 2, 'дециметры': 10 ** 2, 'метры': 1,
                      'километры': 0.001 ** 2, 'гектары': 0.0001},
            'миллиметры': {'миллиметры': 1, 'сантиметры': 0.1 ** 2, 'дециметры': 0.01 ** 2, 'метры': 0.001 ** 2,
                           'километры': 0.000001 ** 2, 'гектары': 0.0000000001},
            'сантиметры': {'миллиметры': 10 ** 2, 'сантиметры': 1, 'дециметры': 0.1 ** 2, 'метры': 0.01 ** 2,
                           'километры': 0.00001 ** 2, 'гектары': 0.000000001},
            'дециметры': {'миллиметры': 100 ** 2, 'сантиметры': 10 ** 2, 'дециметры': 1, 'метры': 0.1 ** 2,
                          'километры': 0.0001 ** 2, 'гектары': 0.00000001},
            'километры': {'миллиметры': 1000000 ** 2, 'сантиметры': 100000 ** 2, 'дециметры': 10000 ** 2,
                          'метры': 1000 ** 2,
                          'километры': 1}, 'гектары': 100}
        self.Data_mass = {'миллиграммы': {'миллиграммы': 1, 'граммы': 1 / 1000, 'килограммы': 0.000001,
                                          'тонны': 0.000000001, 'фунты': 0.000002204623},
                          'граммы': {'миллиграммы': 1000, 'граммы': 1, 'килограммы': 0.001,
                                     'тонны': 0.000001, 'фунты': 0.00220462},
                          'килограммы': {'миллиграммы': 1000000, 'граммы': 1000, 'килограммы': 1,
                                         'тонны': 0.001, 'фунты': 2.204623},
                          'тонны': {'миллиграммы': 1000000000, 'граммы': 1000000, 'килограммы': 1000,
                                    'тонны': 1, 'фунты': 2204.623},
                          'фунты': {'миллиграммы': 453592.4, 'граммы': 453.5924, 'килограммы': 0.4535924,
                                    'тонны': 0.0004535924, 'фунты': 1}}
        self.Data_speed = {'метры в секунду': {'метры в секунду': 1, 'километры в час': 3.6, 'морские узлы': 1.944012},
                           'километры в час': {'метры в секунду': 1, 'километры в час': 0.277778,
                                               'морские узлы': 1.944012},
                           'морские узлы': {'метры в секунду': 0.5144, 'километры в час': 1.85184, 'морские узлы': 1}}
        # вызов каждой кнопки
        self.pushButton_10.clicked.connect(self.num_btn_clicked)
        self.pushButton_9.clicked.connect(self.num_btn_clicked)
        self.pushButton_8.clicked.connect(self.num_btn_clicked)
        self.pushButton_7.clicked.connect(self.num_btn_clicked)
        self.pushButton_6.clicked.connect(self.num_btn_clicked)
        self.pushButton_5.clicked.connect(self.num_btn_clicked)
        self.pushButton_12.clicked.connect(self.num_btn_clicked)
        self.pushButton_11.clicked.connect(self.num_btn_clicked)
        self.pushButton_13.clicked.connect(self.num_btn_clicked)
        self.pushButton_14.clicked.connect(self.num_btn_clicked)
        self.pushButton_16.clicked.connect(self.backspace)
        self.pushButton_18.clicked.connect(self.point)
        self.pushButton_15.clicked.connect(self.bool)
        self.pushButton.clicked.connect(self.calculator)
        self.pushButton_17.clicked.connect(self.convert)
        self.pushButton.clicked.connect(self.calculator)
        self.radioButton.toggled.connect(self.onClicked1)
        self.radioButton_2.toggled.connect(self.onClicked1)
        self.radioButton_3.toggled.connect(self.onClicked1)
        self.radioButton_4.toggled.connect(self.onClicked1)
        self.radioButton_5.toggled.connect(self.onClicked1)
        self.radioButton_6.toggled.connect(self.onClicked1)
        self.listWidget.itemClicked.connect(self.connect_to_journal)

        self.Sort = ''  # показывает что конвертировать, оюъём, длину и тд
        self.input_data = []  # список в который записываются цифры введённые с клавиатуры

    def connect_to_journal(self, item):  # при нажатие на строку в журнале
        self.input_data = []
        aa = item.text().split('\n')[-2].split(' = ')[0]
        self.lcdNumber_3.display(item.text().split('\n')[-2].split(' = ')[0])
        for i in aa:
            self.input_data.append(i)

    def onClicked1(self):  # при нажатии на один из радио баттонов в меню выбора едениц измерения
        #  высвечивается нужная величина, если нажали на длину - метры, сантиметры,
        #  если на объём то метры кубические и тд.
        self.Sort = ''  # показывает что конвертировать, оюъём, длину и тд
        self.Sort = str(self.sender().text())
        if self.Sort == '    Длина':
            self.comboBox.clear()  # добавляет с радиобфттона сорт величин, длину, объём и тд
            self.comboBox_2.clear()
            self.comboBox.addItems(["метры", "миллиметры",
                                    "сантиметры", "дециметры", "километры"])
            self.comboBox_2.addItems(["метры", "миллиметры",
                                      "сантиметры", "дециметры", "километры"])
        elif self.Sort == '    Объём':
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox.addItems(["кубические метры", "кубические миллиметры",
                                    "кубические сантиметры", "кубические дециметры", "литры"])
            self.comboBox_2.addItems(["кубические метры", "кубические миллиметры",
                                      "кубические сантиметры", "кубические дециметры", "литры"])
        elif self.Sort == '   Площадь':
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox.addItems(["метры квадратные", "миллиметры квадратные",
                                    "сантиметры квадратные", "дециметры квадратные", "километры  квадратные",
                                    'гектары'])
            self.comboBox_2.addItems(["метры квадратные", "миллиметры квадратные",
                                      "сантиметры квадратные", "дециметры квадратные", "километры  квадратные",
                                      'гектары'])
        elif self.Sort == '       Вес\n    и масса':
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox.addItems(["миллиграммы", "граммы", "килограммы", "метрические тонны", "фунты"])
            self.comboBox_2.addItems(["миллиграммы", "граммы", "килограммы", "метрические тонны", "фунты"])
        elif self.Sort == 'Температура':
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox.addItems(["°C", "°F", "°K"])
            self.comboBox_2.addItems(["°C", "°F", "°K"])
        elif self.Sort == '   Скорость':
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox.addItems(["метры в секунду", "километры в час", "морские узлы"])
            self.comboBox_2.addItems(["метры в секунду", "километры в час", "морские узлы"])

    def convert(self):  # конвертирует одни единицы в другие, аналог классу равно
        if self.input_data == []:
            self.input_data.append('0')
        first_line = str(self.comboBox.currentText())
        second_line = str(self.comboBox_2.currentText())
        self.today = datetime.datetime.today()
        date = str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))  # дата
        first_line_sogl = ''
        for i in first_line.split(' '):
            comment = morph.parse(i)[0]
            first_line_sogl += comment.make_agree_with_number(float(''.join(self.input_data))).word + ' '
        action = str(float(''.join(self.input_data))) + ' ' + str(first_line_sogl) + 'в ' + second_line
        if self.Sort == '    Длина':
            self.ansver = (float(''.join(self.input_data)) * float(self.Data_length[first_line][second_line]))
            self.lcdNumber_4.display(self.ansver)
            self.listWidget.addItem(QListWidgetItem(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n'))
            self.append_in_journal(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n')
        elif self.Sort == '    Объём':
            self.ansver = float(''.join(self.input_data)) * self.Data_volume[first_line.split(' ')[-1]][
                second_line.split(' ')[-1]]
            self.lcdNumber_4.display(self.ansver)
            self.listWidget.addItem(QListWidgetItem(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n'))
            self.append_in_journal(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n')
        elif self.Sort == '   Площадь':
            self.ansver = float(''.join(self.input_data)) * self.Data_square[first_line.split(' ')[0]][
                second_line.split(' ')[0]]
            self.lcdNumber_4.display(self.ansver)
            self.listWidget.addItem(QListWidgetItem(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n'))
            self.append_in_journal(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n')
        elif self.Sort == '       Вес\n    и масса':
            self.ansver = float(''.join(self.input_data)) * self.Data_mass[first_line.split(' ')[-1]][
                second_line.split(' ')[-1]]
            self.lcdNumber_4.display(self.ansver)
            self.listWidget.addItem(QListWidgetItem(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n'))
            self.append_in_journal(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n')
        elif self.Sort == 'Температура':
            if first_line == '°C' and second_line == '°C':
                self.action_T = '°C в °C'
                self.ansver = float(''.join(self.input_data))
            elif first_line == '°K' and second_line == '°K':
                self.action_T = '°K в °K'
                self.ansver = float(''.join(self.input_data))
            elif first_line == '°F' and second_line == '°F':
                self.action_T = '°F в °F'
                self.ansver = float(''.join(self.input_data))
            elif first_line == '°C' and second_line == '°K':
                self.action_T = '°C в °K'
                self.ansver = float(''.join(self.input_data)) + 273.15
            elif first_line == '°K' and second_line == '°C':
                self.action_T = '°K в °C'
                self.ansver = float(''.join(self.input_data)) - 273.15
            elif first_line == '°C' and second_line == '°F':
                self.action_T = '°C в °F'
                self.ansver = float(''.join(self.input_data)) * 9 / 5 + 32.0
            elif first_line == '°F' and second_line == '°C':
                self.action_T = '°F в °C'
                self.ansver = (float((''.join(self.input_data))) - 32.0) * 5 / 9
            elif first_line == '°K' and second_line == '°F':
                self.action_T = '°K в °F'
                self.ansver = float(''.join(self.input_data)) * 1.8 - 459
            elif first_line == '°F' and second_line == '°K':
                self.action_T = '°F в °K'
                self.ansver = (float(''.join(self.input_data)) + 459.0) / 1.8
            self.lcdNumber_4.display(self.ansver)
            self.listWidget.addItem(
                QListWidgetItem(
                    date + '\n' + str(self.ansver) + ' = ' + str(''.join(self.input_data)) + str(
                        self.action_T) + '\n'))
            self.append_in_journal(
                date + '\n' + str(self.ansver) + ' = ' + str(''.join(self.input_data)) + str(self.action_T) + '\n')
        elif self.Sort == '   Скорость':
            self.ansver = float(''.join(self.input_data)) * self.Data_speed[first_line][second_line]
            self.lcdNumber_4.display(self.ansver)
            self.listWidget.addItem(QListWidgetItem(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n'))
            self.append_in_journal(date + '\n' + str(self.ansver) + ' = ' + str(action) + '\n')

    def num_btn_clicked(self):  # отзывается на нажатие на кнопку на клавиатуре
        if len(self.input_data) <= 14:
            if self.sender().text() != '0':
                self.input_data.append(self.sender().text())
                self.lcdNumber_3.display(float(''.join(self.input_data)))
            else:
                if ''.join(self.input_data) != '0':
                    self.input_data.append('0')
                    if self.input_data[-1] == '0' or self.input_data[-1] == '.':
                        self.lcdNumber_3.display(''.join(self.input_data))
                    else:
                        self.lcdNumber_3.display(float(''.join(self.input_data)))

    def backspace(self):  # удаляет последнюю цифру
        aa = 0
        for i in self.input_data:
            if i != '0' and i != '.':
                aa = 1
        if aa == 0:
            self.input_data = ['0']
            self.lcdNumber_3.display(''.join(self.input_data))
        if len(self.input_data) == 1:
            self.input_data = ['0']
            self.lcdNumber_3.display(''.join(self.input_data))
        else:
            del self.input_data[-1]
            self.lcdNumber_3.display(''.join(self.input_data))

    def point(self):  # ставит точку в водимое число, нельзя поставить дважды
        if len(self.input_data) <= 13:
            if '.' not in self.input_data:
                self.input_data.append('.')
                self.lcdNumber_3.display(''.join(self.input_data))
            elif not self.input_data:
                self.input_data.append('0')
                self.input_data.append('.')
                self.lcdNumber_3.display(''.join(self.input_data))
            elif self.input_data[0] == '0' and self.input_data[1] != '.':
                del self.input_data[0]
                self.lcdNumber_3.display(''.join(self.input_data))

    def bool(self):  # очищает ввод полностью, на клавиатуре кнопка с буквой С
        self.input_data = []
        self.lcdNumber_3.display(float(0))

    def calculator(self):  # возвращает обратно в калькулятор
        self.first_form = FirstForm()
        self.first_form.show()
        self.close()


    def take_a_time(self):
        return str(self.today.strftime("%Y.%m.%d, %H:%M:%S"))

    def append_in_journal(self, element):
        Date = element.split('\n')[0]
        data = float(element.split('\n')[1].split(' = ')[0])
        action = element.split('\n')[1].split(' = ')[1]
        with sqlite3.connect("База_данных/ZZZ.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Jornal(Date, data, action) VALUES('{}', '{}', ' = {}')".format(str(Date), float(data),
                                                                                            str(action)))
            con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.show()
    sys.exit(app.exec())
