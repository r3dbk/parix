import datetime
import sqlite3
import sys
import tkinter as tk
from tkinter import messagebox as mb

from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QGridLayout

from custom_calendar import calendar_widget

calendar = calendar_widget.MainCalendar

root = tk.Tk()
root.withdraw()

conn = sqlite3.connect('parix.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS appointments_db(
    appointment_id TEXT,
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


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('parix.ui', self)
        self.layout = QGridLayout()

        self.frame.setLayout(self.layout)
        self.layout.addWidget(calendar, 0, 0, 0, 0)

        # MainCalendar.setGeometry(QRect(0, 0, 260, 295))


        self.now = QtCore.QTime.fromString('18:00', 'HH:MM')
        self.date = QtCore.QDate.currentDate()

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

        # Resizing columns
        self.tableWidget.setColumnWidth(0, 20)
        self.tableWidget.setColumnWidth(1, 120)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 60)
        self.tableWidget.setColumnWidth(4, 75)
        self.tableWidget.setColumnWidth(5, 80)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(7, 50)
        self.tableWidget.setColumnWidth(8, 70)
        self.tableWidget.setColumnWidth(9, 90)

        self.frame_5.hide()
        self.frame_7.hide()
        self.frame_8.hide()
        self.frame_10.hide()
        self.frame_11.hide()
        self.frame_12.hide()

    def show_app(self):
        self.frame_2.hide()
        self.frame_5.hide()
        self.frame_10.show()

        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Showing appointment')

        one_ges = cur.execute("SELECT * FROM appointments_db;").fetchall()

        sec_ges = cur.execute("SELECT * FROM services_db;").fetchall()

        masters = cur.execute("SELECT * FROM master_db;").fetchall()

        combo_elements = {}

        for master in masters:
            combo_elements[str(master[1] + ' ' + master[2])] = master[0]

        service_array = []
        something = ''

        for master in masters:
            something += str(master[3])

        for service in sec_ges:
            if service[0] in something:
                service_array.append(service[1])

        self.comboBox.clear()
        self.comboBox.addItems(combo_elements)
        self.comboBox.setCurrentText('')

        self.comboBox_2.clear()
        self.comboBox_2.addItems(service_array)
        self.comboBox_2.setCurrentText('')

        try:
            ids = int(one_ges[-1][0]) + 1
        except:
            ids = 0

        self.label_24.setText(str(ids))

    def push_app(self):
        global adm_id

        print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'admin_id is: ' + str(adm_id))

        app_id = self.label_24.text()
        print('test')
        appoint = (str(app_id), self.lineEdit_8.text(),
                   self.lineEdit_9.text(), str(self.timeEdit_3.time().toPyTime()),
                   str(self.calendarWidget.selectedDate().toPyDate()),
                   self.comboBox.currentText(), self.comboBox_2.currentText(), str(adm_id),
                   datetime.datetime.now().strftime('%d-%m-%y'), self.textEdit_2.toPlainText(),)
        print(appoint)
        cur.execute("INSERT INTO appointments_db VALUES(?,?,?,?,?,?,?,?,?,?);", appoint)
        conn.commit()
        self.clear_app()
        self.render_list()

        self.frame_10.hide()
        self.frame_2.show()
        self.frame_5.hide()

    def delete_app(self):
        if self.tableWidget.currentColumn() == 0:
            ap_id = self.tableWidget.currentItem().text()
            print(
                str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (DEL) appoint id is: ' + str(ap_id))

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

            service_array = []
            something = ''
            combo_elements = {}

            ap_id = self.tableWidget.currentItem().text()

            one_ges = cur.execute("SELECT * FROM appointments_db WHERE appointment_id = ?", (str(ap_id),)).fetchall()[0]
            sec_ges = cur.execute("SELECT * FROM services_db;").fetchall()
            masters = cur.execute("SELECT * FROM master_db;").fetchall()

            for master in masters:
                combo_elements[str(master[1] + ' ' + master[2])] = master[0]
                for i in master[3]:
                    if i not in something:
                        something += i

            for service in sec_ges:
                print(service)
                if service[0] in something:
                    service_array.append(sec_ges[1])

            print(service_array, something)

            self.comboBox_3.addItems(service_array)
            self.comboBox_3.setCurrentText('')

            self.comboBox_4.addItems(combo_elements)
            self.comboBox_4.model().item(0).setEnabled(False)
            self.comboBox_4.setCurrentText('')

            self.label_10.setText(self.selected_date_2)

            self.lineEdit_6.clear()
            self.lineEdit_6.setText(str(one_ges[2]))

            self.lineEdit_7.clear()
            self.lineEdit_7.setText(str(one_ges[1]))

            self.timeEdit_2.setTime(
                QtCore.QTime(int(datetime.datetime.strptime(str(one_ges[3]), "%H:%M:%S").strftime("%H")),
                             int(datetime.datetime.strptime(str(one_ges[3]), "%H:%M:%S").strftime("%M"))))

            self.textEdit.setPlainText(one_ges[9])

        else:
            mb.showinfo('Select id', 'To edit an appointment select its id')

    def edit_app(self):
        ap_id = self.tableWidget.currentItem().text()

        print(
            str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (ED) appoint id is: ' + str(ap_id))

        appoint = (self.lineEdit_7.text(),
                   self.lineEdit_6.text(), str(self.timeEdit_2.time().toPyTime()),
                   str(self.calendarWidget_2.selectedDate().toPyDate()),
                   self.comboBox_4.currentText(), self.comboBox_3.currentText(), self.textEdit.toPlainText(),
                   str(ap_id),)

        cur.execute(
            '''UPDATE appointments_db SET firstname = ?, surname = ?, time = ?, date = ?, master_id = ?,
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
            services += '0'
        if self.checkBox_2.isChecked():
            services += '1'
        if self.checkBox_3.isChecked():
            services += '2'
        if self.checkBox_4.isChecked():
            services += '3'
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

            mastr_id = self.tableWidget_2.currentItem().text()

            one_ges = cur.execute("SELECT * FROM master_db WHERE master_id = ?", (str(mastr_id),)).fetchall()[0]

            self.lineEdit_12.setText(str(one_ges[1]))
            self.lineEdit_13.setText(str(one_ges[2]))
            self.label_38.setText(str(one_ges[0]))

            for i in one_ges[3]:
                if i == '0':
                    self.checkBox_5.setChecked(True)
                if i == '1':
                    self.checkBox_6.setChecked(True)
                if i == '2':
                    self.checkBox_7.setChecked(True)
                if i == '3':
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
            services += '0'
        if self.checkBox_6.isChecked():
            services += '1'
        if self.checkBox_7.isChecked():
            services += '2'
        if self.checkBox_8.isChecked():
            services += '3'
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
        one_ges = cur.execute("SELECT * FROM appointments_db;").fetchall()
        sec_ges = cur.execute("SELECT * FROM master_db;").fetchall()
        third_ges = cur.execute("SELECT * FROM services_db;").fetchall()
        self.tableWidget.setRowCount(len(one_ges))
        self.tableWidget_2.setRowCount(len(sec_ges))
        self.tableWidget_4.setRowCount(len(third_ges))
        row_count = 0
        for obj in one_ges:
            column_count = 0
            for elem in obj:
                if column_count == 7:
                    two_ges = cur.execute("SELECT * FROM admin_db WHERE admin_id = ?", (elem,)).fetchall()
                    self.tableWidget.setItem(row_count, column_count, QTableWidgetItem(two_ges[0][1]))
                elif column_count == 4:
                    self.tableWidget.setItem(row_count, column_count, QTableWidgetItem(
                        str(datetime.datetime.strptime(elem, '%Y-%m-%d').strftime('%d %B'))))
                else:
                    self.tableWidget.setItem(row_count, column_count, QTableWidgetItem(str(elem)))
                column_count += 1
            row_count += 1
        row_count_2 = 0
        for obj_2 in sec_ges:
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
        for obj_3 in third_ges:
            column_count_3 = 0
            for elem_3 in obj_3:
                self.tableWidget_4.setItem(row_count_3, column_count_3, QTableWidgetItem(str(elem_3)))
                column_count_3 += 1
            row_count_3 += 1

    def delete_serv(self):
        if self.tableWidget_4.currentRow() != -1:
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

            mastr_id = self.tableWidget_4.currentItem().text()
            print(mastr_id)
            one_ges = cur.execute("SELECT * FROM services_db WHERE service_id = ?", (str(mastr_id),)).fetchall()[0]

            self.lineEdit_16.setText(str(one_ges[1]))
            self.lineEdit_17.setText(str(one_ges[2]))
            self.label_45.setText(str(one_ges[0]))
        else:
            mb.showinfo('Select id', 'To edit service select their id')

    def edit_serv(self):
        ap_id = self.tableWidget_4.currentItem().text()

        print(
            str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ' + 'Selected (ED) service id is: ' + str(ap_id))

        master = (self.lineEdit_16.text(),
                  self.lineEdit_17.text(), ap_id)

        cur.execute(
            "UPDATE master_db SET name = ?, context = ? WHERE service_id = ?;", master)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.exit(app.exec())