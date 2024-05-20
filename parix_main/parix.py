import datetime
import sqlite3
import sys
import tkinter as tk
from tkinter import messagebox as mb
from windows_toasts import Toast, WindowsToaster

from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtCore import QRect, QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QGridLayout, QVBoxLayout

from custom_calendar.calendar_widget import MainCalendar
from table.table_elem import TableElement

# Объедени комбобоксы

root = tk.Tk()
root.withdraw()

conn = sqlite3.connect('parix.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS appointments_db(
    appointment_id TEXT,
    status TEXT,
    firstname TEXT,
    surname TEXT,
    time TEXT,
    date TEXT,
    master_id TEXT,
    service_id TEXT,
    admin_id TEXT,
    when_added TEXT,
    comment TEXT);
    """)

conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS admin_db(
    admin_id TEXT,
    firstname TEXT,
    login TEXT,
    password TEXT);
    """)

conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS master_db(
    master_id TEXT,
    firstname TEXT,
    surname TEXT,
    services TEXT);
    """)

conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS services_db(
    service_id TEXT,
    name TEXT,
    context TEXT);
    """)

conn.commit()


# toaster = WindowsToaster('Python')
# newToast = Toast()
# newToast.text_fields = ['Hello, world!']
# newToast.on_activated = lambda _: print('Toast clicked!')
# toaster.show_toast(newToast)

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('parix.ui', self)
        self.main_menu_layout = QGridLayout()
        self.tab_layout = QGridLayout()

        self.main_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_layout.setSpacing(0)
        self.tab_layout.setContentsMargins(10, 10, 0, 0)

        self.frame.setLayout(self.main_menu_layout)
        self.tab_5.setLayout(self.tab_layout)

        self.calendar = MainCalendar()
        self.calendar.setGeometry(QRect(0, 0, 260, 295))

        self.dict_elem = {}
        self.app_status_dict = {0: 'Active', 1: 'Archived', 2: 'Cancelled'}

        # returns [day(1-31), month(1-12), year(2024)]

        self.main_menu_layout.addWidget(self.calendar, 0, 0)
        self.main_menu_layout.addWidget(self.tabWidget_2, 0, 1)

        self.now = QtCore.QTime.fromString('18:00', 'HH:MM')
        self.date = QtCore.QDate.currentDate()

        self.selected_date = ''
        self.selected_date_2 = ''

        # --------------DELETE WHEN FINISHED---------RETURN FRAME_4 Y-AXIS TO 0!!!---
        self.lineEdit_3.setText('admin')
        self.lineEdit_4.setText('admin')

        self.login()
        # --------------DELETE WHEN FINISHED---------RETURN FRAME_4 Y-AXIS TO 0!!!---

        self.calendarWidget.clicked.connect(self.calendar_clicked)
        self.calendarWidget_2.clicked.connect(self.calendar_2_clicked)

        self.pushButton_6.clicked.connect(self.edit_app)
        self.pushButton_7.clicked.connect(self.login)
        self.pushButton_9.clicked.connect(self.back_app)
        self.pushButton_10.clicked.connect(self.show_edit_app)
        self.pushButton_11.clicked.connect(self.delete_app)
        self.pushButton_12.clicked.connect(self.delete_app)
        self.pushButton_13.clicked.connect(self.render_list)
        self.pushButton_14.clicked.connect(self.show_edit_master)
        self.pushButton_15.clicked.connect(self.delete_master)
        self.pushButton_16.clicked.connect(self.render_list)
        self.pushButton_17.clicked.connect(self.show_app)
        self.pushButton_18.clicked.connect(self.push_app)
        self.pushButton_19.clicked.connect(self.back_app)
        self.pushButton_20.clicked.connect(self.add_master)
        self.pushButton_21.clicked.connect(self.back_master)
        self.pushButton_23.clicked.connect(self.show_add_master)
        self.pushButton_22.clicked.connect(self.edit_master)
        self.pushButton_24.clicked.connect(self.back_master)
        self.pushButton_25.clicked.connect(self.clear_app)
        self.pushButton_26.clicked.connect(self.show_edit_serv)
        self.pushButton_27.clicked.connect(self.delete_serv)
        self.pushButton_28.clicked.connect(self.render_list)
        self.pushButton_29.clicked.connect(self.show_push_serv)
        self.pushButton_30.clicked.connect(self.push_service)
        self.pushButton_31.clicked.connect(self.back_serv)
        self.pushButton_32.clicked.connect(self.edit_serv)
        self.pushButton_33.clicked.connect(self.back_serv)
        self.pushButton_34.clicked.connect(self.delete_master)

        self.comboBox_list = []

        # Resizing columns
        self.tableWidget.setColumnWidth(0, 20)
        self.tableWidget.setColumnWidth(1, 65)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 120)
        self.tableWidget.setColumnWidth(4, 45)
        self.tableWidget.setColumnWidth(5, 55)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(7, 80)
        self.tableWidget.setColumnWidth(8, 40)
        self.tableWidget.setColumnWidth(9, 50)
        self.tableWidget.setColumnWidth(10, 90)

        self.tableWidget_2.setColumnWidth(3, 250)

        self.frame_5.hide()
        self.frame_7.hide()
        self.frame_8.hide()
        self.frame_10.hide()
        self.frame_11.hide()
        self.frame_12.hide()

    def update_tab_app(self, elem):
        ap_id = self.dict_elem[elem][0]

        appoint = (elem.lineEdit.text(),
                   elem.lineEdit_2.text(), str(elem.timeEdit.time().toPyTime()),
                   self.calendar.current_date,
                   elem.comboBox.currentText(), elem.comboBox_2.currentText(),
                   ap_id)

        elem.groupBox.hide()

        cur.execute(
            '''UPDATE appointments_db SET firstname = ?, surname = ?, time = ?, date = ?, master_id = ?,
             service_id = ? WHERE appointment_id = ?''', appoint)
        conn.commit()

        self.render_list()
        self.back_app()

    def cancel_tab_app(self, app_elem):
        print(self.dict_elem)
        app_id = self.dict_elem[app_elem][0]

        cur.execute("UPDATE appointments_db SET status = ? WHERE appointment_id = ?;", ('2', app_id))
        conn.commit()

        app_elem.groupBox.hide()
        self.render_list()

    def archive_tab_app(self, app_elem):
        app_id = self.dict_elem[app_elem][0]

        cur.execute("UPDATE appointments_db SET status = ? WHERE appointment_id = ?;", ('1', app_id))
        conn.commit()

        app_elem.groupBox.hide()
        self.render_list()

    def render_tab_services(self, app_elem, combo_box):
        current_service = self.dict_elem[app_elem][7]
        app_master_id = app_elem.comboBox.currentIndex()

        # redo masters_db, masters id shouldn't be equal to index
        master = cur.execute("SELECT * FROM master_db WHERE master_id = ?;",
                             str(app_master_id, )).fetchall()[0]
        services_db = cur.execute("SELECT * FROM services_db;").fetchall()

        service_array = []
        services = ''

        for i in master[3]:
            if i not in services:
                services += i

        for service in services_db:
            if service[0] in services:
                service_array.append(service[1])

        combo_box.clear()
        combo_box.addItems(service_array)
        combo_box.setCurrentText(current_service)

    def render_combo_box(self, master_box, service_box):
        app_master_id = master_box.currentIndex()
        print(app_master_id)

        # redo masters_db, masters id shouldn't be equal to index
        master = cur.execute("SELECT * FROM master_db WHERE master_id = ?;",
                             str(app_master_id, )).fetchall()[0]
        services_db = cur.execute("SELECT * FROM services_db;").fetchall()

        service_array = []
        services = ''

        for i in master[3]:
            if i not in services:
                services += i

        for service in services_db:
            if service[0] in services:
                service_array.append(service[1])

        service_box.clear()
        service_box.addItems(service_array)

    def show_app(self):
        self.frame_2.hide()
        self.frame_5.hide()
        self.frame_10.show()

        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Showing appointment')

        appointments_db = cur.execute("SELECT * FROM appointments_db;").fetchall()

        masters_db = cur.execute("SELECT * FROM master_db;").fetchall()

        services_id = ''
        masters_name = {}

        for master in masters_db:
            masters_name[str(master[1] + ' ' + master[2])] = master[0]
            for i in master[3]:
                if i not in services_id:
                    services_id += i

        self.comboBox_2.clear()
        self.comboBox_2.addItems(masters_name)

        self.comboBox_2.currentTextChanged.connect(
            lambda state, master_box=self.comboBox_2, service_box=self.comboBox: self.render_combo_box(
                master_box, service_box))

        self.comboBox_2.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(0)

        self.render_combo_box(self.comboBox_2, self.comboBox)

        try:
            ids = int(appointments_db[-1][0]) + 1
        except:
            ids = 0

        self.label_24.setText(str(ids))

    def push_app(self):
        global adm_id

        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'admin_id is: ' + str(adm_id))

        app_id = self.label_24.text()
        appoint = (str(app_id), str(self.comboBox_5.currentIndex()), self.lineEdit_8.text(),
                   self.lineEdit_9.text(), str(self.timeEdit_3.time().toPyTime()),
                   str(self.calendarWidget.selectedDate().toPyDate()),
                   self.comboBox.currentText(), self.comboBox_2.currentText(), str(adm_id),
                   datetime.datetime.now().strftime('%d-%m-%y'), self.textEdit_2.toPlainText(),)
        cur.execute("INSERT INTO appointments_db VALUES(?,?,?,?,?,?,?,?,?,?,?);", appoint)
        conn.commit()
        self.clear_app()
        self.render_list()

        self.frame_10.hide()
        self.frame_2.show()
        self.frame_5.hide()

    def delete_app(self):
        if self.tableWidget.currentColumn() == 0:
            res = mb.askyesno(title='Confirm', message='Are you sure you want to delete this appointment?')
            if res:
                ap_id = self.tableWidget.currentItem().text()
                print(
                    str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (DEL) appoint id is: ' + str(
                        ap_id))

                cur.execute("DELETE FROM appointments_db WHERE appointment_id = ?", (str(ap_id),))
                conn.commit()

                self.render_list()
                self.back_app()
        else:
            mb.showinfo('Select id', 'To delete an appointment select its id')

    def show_edit_app(self):
        if self.tableWidget.currentColumn() == 0:
            print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Showing edit')

            self.frame_2.hide()
            self.frame_5.show()
            self.frame_10.hide()

            ap_id = self.tableWidget.currentItem().text()

            appointment_elem = \
                cur.execute("SELECT * FROM appointments_db WHERE appointment_id = ?", (str(ap_id),)).fetchall()[0]
            masters_db = cur.execute("SELECT * FROM master_db;").fetchall()

            services_id = ''
            masters_name = {}

            for master in masters_db:
                masters_name[str(master[1] + ' ' + master[2])] = master[0]
                for i in master[3]:
                    if i not in services_id:
                        services_id += i

            self.comboBox_4.currentTextChanged.connect(
                lambda state: self.render_combo_box(
                    self.comboBox_4, self.comboBox_3))

            self.comboBox_4.clear()
            self.comboBox_4.addItems(masters_name)

            self.comboBox_3.setCurrentIndex(0)
            self.comboBox_4.setCurrentIndex(0)

            self.render_combo_box(self.comboBox_4, self.comboBox_3)

            self.comboBox_6.setCurrentIndex(int(appointment_elem[1]))

            self.label_10.setText(self.selected_date_2)
            self.label_17.setText(appointment_elem[0])

            self.lineEdit_6.setText(str(appointment_elem[3]))
            self.lineEdit_7.setText(str(appointment_elem[2]))

            self.timeEdit_2.setTime(
                QtCore.QTime(int(datetime.datetime.strptime(str(appointment_elem[4]), "%H:%M:%S").strftime("%H")),
                             int(datetime.datetime.strptime(str(appointment_elem[4]), "%H:%M:%S").strftime("%M"))))

            self.textEdit.setPlainText(appointment_elem[10])

        else:
            mb.showinfo('Select id', 'To edit an appointment select its id')

    def edit_app(self):
        ap_id = self.tableWidget.currentItem().text()

        print(
            str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (ED) appoint id is: ' + str(ap_id))

        appoint = (str(self.comboBox_6.currentIndex()), self.lineEdit_7.text(),
                   self.lineEdit_6.text(), str(self.timeEdit_2.time().toPyTime()),
                   str(self.calendarWidget_2.selectedDate().toPyDate()),
                   self.comboBox_4.currentText(), self.comboBox_3.currentText(), self.textEdit.toPlainText(),
                   str(ap_id),)

        cur.execute(
            '''UPDATE appointments_db SET status = ?, firstname = ?, surname = ?, time = ?, date = ?, master_id = ?,
             service_id = ?, comment = ? WHERE appointment_id = ?''', appoint)
        conn.commit()

        self.render_list()
        self.back_app()

    def back_app(self):
        self.frame_2.show()
        self.frame_5.hide()
        self.frame_10.hide()

        self.lineEdit_6.hide()
        self.lineEdit_7.hide()

    def back_master(self):
        self.frame_8.hide()
        self.frame_7.hide()
        self.frame_6.show()
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')

    def clear_app(self):
        self.lineEdit_8.setText('')
        self.lineEdit_9.setText('')
        self.timeEdit_3.setTime(self.now)
        self.calendarWidget.setSelectedDate(self.date)
        self.comboBox.setCurrentText('')
        self.comboBox_2.setCurrentText('')
        self.textEdit_2.setPlainText('')
        self.calendar_clicked()

    def clean_serv(self):
        self.lineEdit_16.setText('')
        self.lineEdit_17.setText('')
        self.lineEdit_14.setText('')
        self.lineEdit_15.setText('')

    def back_serv(self):
        self.frame_9.show()
        self.frame_11.hide()
        self.frame_12.hide()

    def show_login(self):
        self.frame_4.show()

    def show_add_master(self):
        global master_id

        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'admin_id is: ' + str(adm_id))

        self.frame_8.hide()
        self.frame_7.show()
        self.frame_6.hide()

        one_ges = cur.execute("SELECT * FROM master_db;").fetchall()

        try:
            master_id = int(one_ges[-1][0]) + 1
        except:
            master_id = 0

        self.label_34.setText(str(master_id))

    def add_master(self):
        services = ''
        # checkBox_list = {self.checkBox: 0, self.checkBox_2: 1, self.checkBox_3: 2, self.checkBox_4: 3, }

        # --------RE-DO-----------
        if self.checkBox.isChecked():
            services += '1'
        if self.checkBox_2.isChecked():
            services += '2'
        if self.checkBox_3.isChecked():
            services += '3'
        if self.checkBox_4.isChecked():
            services += '4'
        # ---------RE-DO----------

        # for key, value in checkBox_list.items():
        #     if self.key.isChecked():
        #         services += value

        master = (str(master_id), self.lineEdit_10.text(),
                  self.lineEdit_11.text(), services)

        cur.execute("INSERT INTO master_db VALUES(?,?,?,?);", master)
        conn.commit()

        self.render_list()
        self.back_master()

    def show_edit_master(self):
        if self.tableWidget_2.currentColumn() == 0:

            self.frame_8.show()
            self.frame_7.hide()
            self.frame_6.hide()

            master_key = self.tableWidget_2.currentItem().text()

            master_elem = cur.execute("SELECT * FROM master_db WHERE master_id = ?", (str(master_key),)).fetchall()[0]

            self.lineEdit_12.setText(str(master_elem[1]))
            self.lineEdit_13.setText(str(master_elem[2]))
            self.label_38.setText(str(master_elem[0]))

            for i in master_elem[3]:
                if i == '1':
                    self.checkBox_5.setChecked(True)
                if i == '2':
                    self.checkBox_6.setChecked(True)
                if i == '3':
                    self.checkBox_7.setChecked(True)
                if i == '4':
                    self.checkBox_8.setChecked(True)
        else:
            mb.showinfo('Select id', 'To edit master select their id')

    def edit_master(self):
        ap_id = self.tableWidget_2.currentItem().text()
        print(
            str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (ED) master id is: ' + str(ap_id))
        services = ''
        # --------RE-DO-----------
        if self.checkBox_5.isChecked():
            services += '1'
        if self.checkBox_6.isChecked():
            services += '2'
        if self.checkBox_7.isChecked():
            services += '3'
        if self.checkBox_8.isChecked():
            services += '4'
        # ---------RE-DO----------
        master = (self.lineEdit_12.text(),
                  self.lineEdit_13.text(), services, ap_id)
        cur.execute(
            '''UPDATE master_db SET firstname = ?, surname = ?, services = ? WHERE master_id = ?''', master)
        conn.commit()
        self.render_list()
        self.back_master()

    def delete_master(self):
        if self.tableWidget_2.currentRow() != -1:
            res = mb.askyesno(title='Confirm', message='Are you sure you want to delete this master?')
            if res:
                ap_id = self.tableWidget_2.currentItem().text()
                print(
                    str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (DEL) master id is: ' + str(
                        ap_id))
                cur.execute("DELETE FROM master_db WHERE master_id = ?", (str(ap_id),))
                conn.commit()
                self.render_list()
                self.back_master()
        else:
            mb.showinfo('Select id', 'To delete master from the database select its id')

    def login(self):
        global adm_id
        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Login button pressed')
        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'One_ges is: ' + str(
            cur.execute("SELECT * FROM admin_db;").fetchall()))
        one_ges = cur.execute("SELECT * FROM admin_db;").fetchall()
        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'One_ges is: ' + str(one_ges))
        for element in one_ges:
            print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Login for cycle')
            if self.lineEdit_3.text().lower() in element:
                if self.lineEdit_4.text() == element[3]:
                    self.frame_4.hide()
                    adm_id = element[0]
                    self.render_list()
                    break
                else:
                    print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Wrong password')
                    self.label_9.setText('Wrong password')
            else:
                print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Login does not exist')
                self.label_9.setText('Check login')

    def render_list(self):
        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Render')

        appointments_db = cur.execute("SELECT * FROM appointments_db;").fetchall()
        masters_db = cur.execute("SELECT * FROM master_db;").fetchall()
        services_db = cur.execute("SELECT * FROM services_db;").fetchall()

        self.tableWidget.setRowCount(len(appointments_db))
        self.tableWidget_2.setRowCount(len(masters_db))
        self.tableWidget_4.setRowCount(len(services_db))

        self.dict_elem = {}
        for i in reversed(range(self.tab_layout.count())):
            self.tab_layout.itemAt(i).widget().setParent(None)

        current_tab_row = 0

        if len(appointments_db) > 0:
            # Rendering appointments on the main page
            for app_2 in appointments_db:
                if app_2[1] != '0':
                    pass
                else:
                    app_elem = TableElement()
                    self.dict_elem[app_elem] = app_2

                    app_elem.pushButton.clicked.connect(lambda state, x=app_elem: self.cancel_tab_app(x))
                    app_elem.pushButton_3.clicked.connect(lambda state, x=app_elem: self.archive_tab_app(x))
                    app_elem.pushButton_4.clicked.connect(lambda state, x=app_elem: self.update_tab_app(x))

                    # If absolute
                    # app_vertical_pos = len(self.dict_elem) * 51 + len(self.dict_elem) * 20 + 10

                    app_elem.setGeometry(QRect(10, 10, 365, 51))

                    app_elem.comboBox_2.currentTextChanged.connect(
                        lambda state: app_elem.label_6.setText(app_elem.comboBox_2.currentText()))

                    services_id = ''
                    masters_name = {}

                    for master in masters_db:
                        masters_name[str(master[1] + ' ' + master[2])] = master[0]
                        for i in master[3]:
                            if i not in services_id:
                                services_id += i

                    app_elem.comboBox.currentTextChanged.connect(
                        lambda state, tab_elem=app_elem, combo_box=app_elem.comboBox_2: self.render_tab_services(
                            tab_elem, combo_box))

                    app_elem.comboBox.clear()

                    app_elem.comboBox.addItems(masters_name)

                    app_elem.comboBox.setCurrentText(app_2[6])
                    app_elem.comboBox_2.setCurrentText(app_2[7])

                    self.render_tab_services(app_elem, app_elem.comboBox_2)

                    app_elem.lineEdit.setText(app_2[2])
                    app_elem.lineEdit_2.setText(app_2[3])

                    app_elem.label.setText(datetime.datetime.strptime(app_2[4], '%H:%M:%S').strftime('%H:%M'))  # re-do
                    app_elem.label_2.setText(
                        datetime.datetime.strptime(app_2[5], '%Y-%m-%d').strftime('%d %B'))
                    app_elem.label_4.setText(app_2[2] + ' ' + app_2[3])
                    app_elem.label_9.setText(
                        datetime.datetime.strptime(app_2[5], '%Y-%m-%d').strftime('%d %B'))

                    app_elem.timeEdit.setTime(datetime.datetime.strptime(app_2[4], '%H:%M:%S').time())

                    self.tab_layout.addWidget(app_elem, current_tab_row, 0)
                    # self.tab_layout.setRowStretch(current_tab_row, 2)
                    # self.tab_layout.setRowStretch(current_tab_row+1, 10-len(self.dict_elem))

                    current_tab_row += 1

        row_count = 0
        for obj in appointments_db:
            column_count = 0
            for elem in obj:
                if column_count == 8:
                    two_ges = cur.execute("SELECT * FROM admin_db WHERE admin_id = ?", (elem,)).fetchall()
                    self.tableWidget.setItem(row_count, column_count, QTableWidgetItem(two_ges[0][1]))
                elif column_count == 5:
                    self.tableWidget.setItem(row_count, column_count, QTableWidgetItem(
                        str(datetime.datetime.strptime(elem, '%Y-%m-%d').strftime('%d %B'))))
                elif column_count == 4:
                    self.tableWidget.setItem(row_count, column_count, QTableWidgetItem(
                        str(datetime.datetime.strptime(elem, '%H:%M:%S').strftime('%H:%M'))))
                elif column_count == 1:
                    app_status = self.app_status_dict[int(elem)]
                    self.tableWidget.setItem(row_count, column_count, QTableWidgetItem(
                        str(app_status)))
                else:
                    self.tableWidget.setItem(row_count, column_count, QTableWidgetItem(str(elem)))
                column_count += 1
            row_count += 1
        row_count_2 = 0
        for obj_2 in masters_db:
            column_count_2 = 0
            for elem_2 in obj_2:
                if column_count_2 == 3:
                    services = []
                    for elem in elem_2:
                        if elem == '1':
                            services.append('Стрижка')
                        if elem == '2':
                            services.append('Укладка')
                        if elem == '3':
                            services.append('Окрашивание')
                        if elem == '4':
                            services.append('Уход')

                    self.tableWidget_2.setItem(row_count_2, column_count_2,
                                               QTableWidgetItem(', '.join(services).capitalize()))
                else:
                    self.tableWidget_2.setItem(row_count_2, column_count_2, QTableWidgetItem(str(elem_2)))
                column_count_2 += 1
            row_count_2 += 1
        row_count_3 = 0
        for obj_3 in services_db:
            column_count_3 = 0
            for elem_3 in obj_3:
                self.tableWidget_4.setItem(row_count_3, column_count_3, QTableWidgetItem(str(elem_3)))
                column_count_3 += 1
            row_count_3 += 1

    def delete_serv(self):
        if self.tableWidget_4.currentRow() != -1:
            res = mb.askyesno(title='Confirm', message='Are you sure you want to delete this service?')
            if res:
                ap_id = self.tableWidget_4.currentItem().text()
                print(
                    str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (DEL) service id is: ' + str(
                        ap_id))
                cur.execute("DELETE FROM services_db WHERE service_id = ?", (str(ap_id),))
                conn.commit()
                self.render_list()
                self.back_app()
        else:
            mb.showinfo('Select id', 'To delete service from the database select its id')

    def show_push_serv(self):
        self.frame_9.hide()
        self.frame_11.show()
        self.frame_12.hide()

        one_ges = cur.execute("SELECT * FROM services_db;").fetchall()

        try:
            master_id = int(one_ges[-1][0]) + 1
        except:
            master_id = 0

        self.label_42.setText(str(master_id))

    def push_service(self):
        one_ges = cur.execute("SELECT * FROM services_db;").fetchall()

        try:
            master_id = int(one_ges[-1][0]) + 1
        except:
            master_id = 0

        master = (str(master_id), self.lineEdit_14.text(),
                  self.lineEdit_15.text())

        self.label_42.setText(str(master_id))

        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Service is: ' + str(master))

        cur.execute("INSERT INTO services_db VALUES(?,?,?);", master)
        conn.commit()

        self.back_serv()
        self.clean_serv()
        self.render_list()

    def show_edit_serv(self):
        if self.tableWidget_4.currentColumn() == 0:
            self.frame_12.show()
            self.frame_11.hide()
            self.frame_9.hide()

            master_key = self.tableWidget_4.currentItem().text()
            service_elem = cur.execute("SELECT * FROM services_db WHERE service_id = ?",
                                       (str(master_key),)).fetchall()[0]

            self.lineEdit_16.setText(str(service_elem[1]))
            self.lineEdit_17.setText(str(service_elem[2]))
            self.label_45.setText(str(service_elem[0]))
        else:
            mb.showinfo('Select id', 'To edit service select their id')

    def edit_serv(self):
        ap_id = self.tableWidget_4.currentItem().text()

        print(
            str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (ED) service id is: ' + str(ap_id))

        master = (self.lineEdit_16.text(),
                  self.lineEdit_17.text(), ap_id)

        cur.execute(
            "UPDATE services_db SET name = ?, context = ? WHERE service_id = ?;", master)
        conn.commit()

        self.render_list()
        self.back_serv()
        self.clean_serv()

    def calendar_clicked(self):
        self.selected_date = self.calendarWidget.selectedDate().toPyDate()

        self.label_19.setText(self.selected_date.strftime('%d %B'))

        print(str(self.selected_date))

    def calendar_2_clicked(self):
        self.selected_date_2 = self.calendarWidget_2.selectedDate().toPyDate()

        self.label_10.setText(self.selected_date_2.strftime('%d %B'))

        print(str(self.selected_date_2))


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = exception_hook
    sys.exit(app.exec())
