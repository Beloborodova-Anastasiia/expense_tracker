import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from utils import handle_transactions_file


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setWindowTitle('Expense Tracker')
        self.setGeometry(300, 300, 2000, 1200)
        self.create_appearance()
        self.show()

    def create_appearance(self):
        self.label('Enter you name: ', [50, 50])
        self.form([400, 50])
        self.label('Enter file name', [50, 150])
        self.form([400, 150])
        self.button(' Download transactions ', [50, 250])

    def label(self, text: str, position: list):
        lbl = QtWidgets.QLabel(self)
        lbl.setText(text)
        lbl.setFont(QtGui.QFont('Arial', 14))
        lbl.adjustSize()
        lbl.move(*position)

    def form(self, position: list):
        form = QtWidgets.QLineEdit(self)
        form.setFont(QtGui.QFont('Arial', 14))
        form.adjustSize()
        form.move(*position)

    def button(self, text: str, position: list,):
        btn = QtWidgets.QPushButton(self)
        btn.setFont(QtGui.QFont('Arial', 14))
        btn.setText(text)
        btn.adjustSize()
        btn.move(*position)


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(300, 300, 2000, 1200)
    win.setWindowTitle('Expense Tracker')
    # win.setToolTip('ExpenseTracker')

    lbl_name = QtWidgets.QLabel(win)
    lbl_name.setText('Enter you name: ', )
    lbl_name.move(100, 500)
 
    win.show()
    sys.exit(app.exec_())


def main():
    # handle_transactions_file()
    app = QtWidgets.QApplication(sys.argv)
    application = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
