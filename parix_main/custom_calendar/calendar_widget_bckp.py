import calendar
import datetime
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calendar.ui', self)

        # Dictionary which contains buttons and their status
        # day(1-31), month(1-12), year(23,24,25 etc.), active(T/F), weekday/weekend(T/F), selected(T/F), for example [7, 03, 24, True, True, False]
        self.buttons = {self.btn_1: [0, 0, 0, False, False, False], self.btn_2: [0, 0, 0, False, False, False],
                        self.btn_3: [0, 0, 0, False, False, False], self.btn_4: [0, 0, 0, False, False, False],
                        self.btn_5: [0, 0, 0, False, False, False], self.btn_6: [0, 0, 0, False, False, False],
                        self.btn_7: [0, 0, 0, False, False, False], self.btn_8: [0, 0, 0, False, False, False],
                        self.btn_9: [0, 0, 0, False, False, False], self.btn_10: [0, 0, 0, False, False, False],
                        self.btn_11: [0, 0, 0, False, False, False], self.btn_12: [0, 0, 0, False, False, False],
                        self.btn_13: [0, 0, 0, False, False, False], self.btn_14: [0, 0, 0, False, False, False],
                        self.btn_15: [0, 0, 0, False, False, False], self.btn_16: [0, 0, 0, False, False, False],
                        self.btn_17: [0, 0, 0, False, False, False], self.btn_18: [0, 0, 0, False, False, False],
                        self.btn_19: [0, 0, 0, False, False, False], self.btn_20: [0, 0, 0, False, False, False],
                        self.btn_21: [0, 0, 0, False, False, False], self.btn_22: [0, 0, 0, False, False, False],
                        self.btn_23: [0, 0, 0, False, False, False], self.btn_24: [0, 0, 0, False, False, False],
                        self.btn_25: [0, 0, 0, False, False, False], self.btn_26: [0, 0, 0, False, False, False],
                        self.btn_27: [0, 0, 0, False, False, False], self.btn_28: [0, 0, 0, False, False, False],
                        self.btn_29: [0, 0, 0, False, False, False], self.btn_30: [0, 0, 0, False, False, False],
                        self.btn_31: [0, 0, 0, False, False, False], self.btn_32: [0, 0, 0, False, False, False],
                        self.btn_33: [0, 0, 0, False, False, False], self.btn_34: [0, 0, 0, False, False, False],
                        self.btn_35: [0, 0, 0, False, False, False], self.btn_36: [0, 0, 0, False, False, False],
                        self.btn_37: [0, 0, 0, False, False, False], self.btn_38: [0, 0, 0, False, False, False],
                        self.btn_39: [0, 0, 0, False, False, False], self.btn_40: [0, 0, 0, False, False, False],
                        self.btn_41: [0, 0, 0, False, False, False], self.btn_42: [0, 0, 0, False, False, False]}

        # -- Styles --

        self.comboBox.setStyleSheet("""
            QComboBox {
                border: none;
            }
            QComboBox::drop-down:button {
                border:none;
                background:none;
            }
            QComboBox QAbstractItemView {
                border: none;
            }
        """)

        self.comboBox_2.setStyleSheet("""
            QComboBox {
                border: none;
            }
            QComboBox::drop-down:button {
                border: none;
                background:none;
            }
            QComboBox QAbstractItemView {
                border: none;
            }
        """)

        # Adding years
        first_year = 2023
        for i in range(3):
            self.comboBox_2.addItem(str(first_year))
            first_year += 1

        # -- Connect --

        self.pushButton.clicked.connect(lambda state, direction='l': self.switch_month(direction))
        self.pushButton_2.clicked.connect(lambda state, direction='r': self.switch_month(direction))

        self.comboBox.currentIndexChanged.connect(self.render_month)
        self.comboBox_2.currentIndexChanged.connect(self.render_month)

        # Rendering current date
        self.comboBox.setCurrentIndex(int(datetime.datetime.now().strftime('%m')) - 1)
        self.comboBox_2.setCurrentText(str(datetime.datetime.now().year))
        self.label_8.setText(str(datetime.datetime.now().strftime('%d')))

    def switch_month(self, direction):
        print('Switching month to the:', direction)
        current_month_idx = self.comboBox.currentIndex()
        current_year_idx = self.comboBox_2.currentIndex()

        if direction == 'l':
            if current_month_idx > 0:
                self.comboBox.setCurrentIndex(current_month_idx - 1)
            else:
                self.comboBox_2.setCurrentIndex(current_year_idx - 1)
                self.comboBox.setCurrentIndex(11)

        elif direction == 'r':
            if current_month_idx < 11:
                self.comboBox.setCurrentIndex(current_month_idx + 1)
            else:
                self.comboBox_2.setCurrentIndex(current_year_idx + 1)
                self.comboBox.setCurrentIndex(0)

    def render_month(self):
        # print('Current month index:', self.comboBox.currentIndex())
        # print('Current year:', self.comboBox_2.currentText())
        year = int(self.comboBox_2.currentText())
        month = self.comboBox.currentIndex() + 1

        # Defying and setting first weekday of selected month
        calendar.setfirstweekday(datetime.date(year, month, 1).weekday())
        first_weekday = calendar.firstweekday()

        # Number of days in selected month
        days_num = calendar.monthrange(year, month)[1]
        print(first_weekday + days_num)

        # If first weekday is not Monday
        if first_weekday != 0:

            # Number of days in previous month
            # If it's January
            if month == 1:
                prev_days_num = calendar.monthrange(year - 1, 12)[1]
            # All other months
            else:
                prev_days_num = calendar.monthrange(year, month - 1)[1]

            prev_days_num -= first_weekday - 1

            # Separate variable for cycle
            day = prev_days_num

            # rendering previous month's btns
            for tup in list(self.buttons.items())[:first_weekday]:
                btn = tup[0]

                if month == 1:
                    day_of_week = datetime.date(year - 1, 12, day).weekday()
                else:
                    day_of_week = datetime.date(year, month - 1, day).weekday()

                # If its weekend
                if day_of_week == 5 or day_of_week == 6:
                    try:
                        btn.clicked.disconnect()
                    except:
                        pass
                    btn.setText(str(day))
                    btn.setStyleSheet("""
                    QPushButton {
                        border: 2px solid #a76666;
                        border-radius: 10px;
                        font-size: 10pt;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        border-color: #c65757;
                    }
                    """)
                    btn.clicked.connect(lambda state, button=btn: self.day_selected(button))

                    # day(1-31), month(1-12), year(23,24,25 etc.), active(T/F), weekday/weekend(T/F), selected(T/F), for example [7, 03, 24, True, True, False]
                    if month == 1:
                        self.buttons[btn][0] = day
                        self.buttons[btn][1] = 12
                        self.buttons[btn][2] = year - 1
                        self.buttons[btn][3] = False
                        self.buttons[btn][4] = False
                    else:
                        self.buttons[btn][0] = day
                        self.buttons[btn][1] = month - 1
                        self.buttons[btn][2] = year
                        self.buttons[btn][3] = False
                        self.buttons[btn][4] = False
                    day += 1

                # if its weekday
                else:
                    try:
                        btn.clicked.disconnect()
                    except:
                        pass
                    btn.setText(str(day))
                    btn.setStyleSheet("""
                    QPushButton {
                        border: 2px solid #6b7aa7;
                        border-radius: 10px;
                        font-size: 10pt;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        border-color: #4479cf;
                    }
                    """)
                    btn.clicked.connect(lambda state, button=btn: self.day_selected(button))

                    # day(1-31), month(1-12), year(23,24,25 etc.), active(T/F), weekday/weekend(T/F), selected(T/F), for example [7, 03, 24, True, True, False]
                    if month == 1:
                        self.buttons[btn][0] = day
                        self.buttons[btn][1] = 12
                        self.buttons[btn][2] = year - 1
                        self.buttons[btn][3] = False
                        self.buttons[btn][4] = True
                    else:
                        self.buttons[btn][0] = day
                        self.buttons[btn][1] = month - 1
                        self.buttons[btn][2] = year
                        self.buttons[btn][3] = False
                        self.buttons[btn][4] = True
                    day += 1

        # Rendering active buttons
        day = 1
        for tup in list(self.buttons.items())[first_weekday:days_num + first_weekday]:
            btn = tup[0]
            day_of_week = datetime.date(year, month, day).weekday()

            # If its weekend
            if day_of_week == 5 or day_of_week == 6:
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                btn.setText(str(day))
                btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #ffb4b4;
                    border-radius: 10px;
                    font-size: 10pt;
                    font-weight: 600;
                }
                QPushButton:hover {
                    border-color: #ff8e8e;
                }
                """)
                btn.clicked.connect(lambda state, button=btn: self.day_selected(button))

                self.buttons[btn][0] = day
                self.buttons[btn][1] = month
                self.buttons[btn][2] = year
                self.buttons[btn][3] = True
                self.buttons[btn][4] = False

            # if its weekday
            else:
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                btn.setText(str(day))
                btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #a4b9ff;
                    border-radius: 10px;
                    font-size: 10pt;
                    font-weight: 600;
                }
                QPushButton:hover {
                    border-color: #7b9aff;
                }
                """)
                btn.clicked.connect(lambda state, button=btn: self.day_selected(button))

                self.buttons[btn][0] = day
                self.buttons[btn][1] = month
                self.buttons[btn][2] = year
                self.buttons[btn][3] = True
                self.buttons[btn][4] = True
            day += 1

        # Rendering the rest of disabled buttons
        day = 1

        # If there's not enough days to fulfill the 6th row, we disable them
        if first_weekday + days_num <= 35:
            leftovers = 35
            for tup in list(self.buttons.items())[leftovers:]:
                try:
                    tup[0].clicked.disconnect()
                except:
                    pass
                tup[0].setText('')
                tup[0].setStyleSheet("""
                QPushButton {
                    border: 2px solid #c1c1c1;
                    background-color: #ffffff;
                    border-radius: 10px;
                }
                """)
        else:
            leftovers = 42

        for tup in list(self.buttons.items())[days_num + first_weekday:leftovers]:
            btn = tup[0]

            if month == 12:
                day_of_week = datetime.date(year + 1, 1, day).weekday()
            else:
                day_of_week = datetime.date(year, month + 1, day).weekday()

            # If its weekend
            if day_of_week == 5 or day_of_week == 6:
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                btn.setText(str(day))
                btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #a76666;
                    border-radius: 10px;
                    font-size: 10pt;
                    font-weight: 600;
                }
                QPushButton:hover {
                    border-color: #c65757;
                }
                """)
                btn.clicked.connect(lambda state, button=btn: self.day_selected(button))

                # day(1-31), month(1-12), year(23,24,25 etc.), active(T/F), weekday/weekend(T/F), selected(T/F),
                # for example [7, 03, 24, True, True, False]
                if month == 12:
                    self.buttons[btn][0] = day
                    self.buttons[btn][1] = 1
                    self.buttons[btn][2] = year + 1
                    self.buttons[btn][3] = False
                    self.buttons[btn][4] = False
                else:
                    self.buttons[btn][0] = day
                    self.buttons[btn][1] = month + 1
                    self.buttons[btn][2] = year
                    self.buttons[btn][3] = False
                    self.buttons[btn][4] = False
            # if its weekday
            else:
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                btn.setText(str(day))
                btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #6b7aa7;
                    border-radius: 10px;
                    font-size: 10pt;
                    font-weight: 600;
                }
                QPushButton:hover {
                    border-color: #4479cf;
                }
                """)
                btn.clicked.connect(lambda state, button=btn: self.day_selected(button))

                if month == 12:
                    self.buttons[btn][0] = day
                    self.buttons[btn][1] = 1
                    self.buttons[btn][2] = year + 1
                    self.buttons[btn][3] = False
                    self.buttons[btn][4] = True
                else:
                    self.buttons[btn][0] = day
                    self.buttons[btn][1] = month + 1
                    self.buttons[btn][2] = year
                    self.buttons[btn][3] = False
                    self.buttons[btn][4] = True
            day += 1

    # day(1-31), month(1-12), year(23,24,25 etc.), active(T/F), weekday/weekend(T/F), selected(T/F),
    # for example [7, 3, 24, True, True, False]

    def day_selected(self, btn):
        # 1-12
        current_month = self.comboBox.currentIndex() + 1

        for tup in list(self.buttons.items()):

            # When matching btn found in the list
            if btn == tup[0]:

                # writing old button info in the new variable, so button info stays constant
                btn_info = []
                for info in self.buttons[btn]:
                    btn_info.append(info)

                # If btn is active (within current month range)
                if self.buttons[btn][3]:
                    self.render_month()
                    self.label_8.setText(str(btn_info[0]))
                    self.label_8.setStyleSheet(
                        u'border: 2px solid red;\nborder-radius: 0;\nbackground-color: none;\nbackground:none;')
                    btn.setStyleSheet("""
                    QPushButton {
                        border: 2px solid #ff4c4c;
                        border-radius: 0;
                        font-size: 10pt;
                        font-weight: 600;
                    }
                    """)

                    # Selected - true
                    self.buttons[btn][5] = True

                # If btn is disabled (out of current month range)
                else:

                    # Determining which month to switch to (previous or next)

                    if current_month > btn_info[1]:
                        # Exception in case we're switching from Jan to Dec via day-button
                        if int(self.comboBox_2.currentText()) < btn_info[2]:
                            self.switch_month('r')
                        else:
                            # Switching to the previous month
                            self.switch_month('l')
                    else:
                        # Exception in case we're switching from Dec to Jan via day-button
                        if int(self.comboBox_2.currentText()) > btn_info[2]:
                            self.switch_month('l')
                        else:
                            # Switching to the next month
                            self.switch_month('r')

                    # Finding the button which has to be selected in the updated page
                    for tup_2 in list(self.buttons.items()):
                        if self.buttons[tup_2[0]][3] and self.buttons[tup_2[0]][0] == btn_info[0]:
                            self.label_8.setText(str(tup_2[1][0]))
                            self.label_8.setStyleSheet(
                                u'border: 2px solid red;\nborder-radius: 0;\nbackground-color: none;\nbackground:none;')
                            tup_2[0].setStyleSheet(
                                u"border: 2px solid red;\nborder-radius: 0;\nfont-size:10pt;\nfont-weight:600;")

                            # Selected - true
                            self.buttons[tup_2[0]][5] = True
                            break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.exit(app.exec())
