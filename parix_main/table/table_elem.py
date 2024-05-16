import datetime
import sys
from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QGridLayout


class TableElement(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./table/tabel_elem.ui', self)

        self.pushButton_2.clicked.connect(self.show_edit)
        self.pushButton_5.clicked.connect(self.hide_edit)

        self.comboBox.currentTextChanged.connect(lambda state: self.label_5.setText(self.comboBox.currentText()))
        self.comboBox_2.currentTextChanged.connect(lambda state: self.label_6.setText(self.comboBox_2.currentText()))

        self.groupBox.hide()

    def show_edit(self):
        self.groupBox.show()

    def hide_edit(self):
        self.groupBox.hide()


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableElement()
    ex.show()
    sys.excepthook = exception_hook
    sys.exit(app.exec())
