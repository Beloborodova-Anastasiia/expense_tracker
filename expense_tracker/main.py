# import sys
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from utils import handle_transactions_file


def main():
    handle_transactions_file()
    # app = QtWidgets.QApplication(sys.argv)
    # application = App()
    # sys.exit(app.exec_())


if __name__ == '__main__':
    main()
