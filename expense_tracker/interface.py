# import sys

# from PyQt5 import Qt, QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow


# class App(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(App, self).__init__()
#         self.setWindowTitle('Expense Tracker')
#         self.setGeometry(300, 300, 2000, 1200)
#         self.label_user = self.label('Enter you name: ', [50, 50])
#         self.form_user = self.form([400, 50])
#         self.label_file = self.label('Enter file name', [50, 150])
#         self.form_file = self.form([400, 150])
#         self.button_start = self.button(' Start calculations ', [50, 250])
#         self.show()

#     def label(self, text: str, position: list):
#         lbl = QtWidgets.QLabel(self)
#         lbl.setText(text)
#         lbl.setFont(QtGui.QFont('Arial', 14))
#         lbl.adjustSize()
#         lbl.move(*position)
#         return lbl

#     def form(self, position: list):
#         form = QtWidgets.QLineEdit(self)
#         form.setFont(QtGui.QFont('Arial', 14))
#         form.adjustSize()
#         form.move(*position)
#         return form

#     def button(self, text: str, position: list,):
#         btn = QtWidgets.QPushButton(self)
#         btn.setFont(QtGui.QFont('Arial', 14))
#         btn.setText(text)
#         btn.adjustSize()
#         btn.move(*position)
#         btn.clicked.connect(self.take)
#         return btn

#     def take(self, pressed):
#         user = self.form_user.text()
#         file = self.form_file.text()
#         handle_transactions_file(user, file)
#         self.label_user = self.label('Done: ', [50, 350])

#         print(user, file)
#         return user, file
