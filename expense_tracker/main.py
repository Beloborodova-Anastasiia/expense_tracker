# import sys
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5 import QtGui, QtWidgets, QtCore, Qt
from utils import (create_database, create_session,  handle_transactions_file,
                   import_to_csv, extract_categories)
from models import Accumulation, Average, Spending, Summary, Transaction
from constants import LANGUAGES


def main():
    engine = create_database('sqlite:///tranasactions.db', Transaction)
    session = create_session(engine)
    handle_transactions_file(session)
    # app = QtWidgets.QApplication(sys.argv)
    # application = App()
    # sys.exit(app.exec_())
    while True:
        language = input('Enter output language (en or ru): \n')
        if language in LANGUAGES:
            break
        else:
            print('Invalid value \n')

    import_to_csv(session, Summary, language)
    import_to_csv(session, Average, language)
    import_to_csv(session, Accumulation, language)
    import_to_csv(session, Spending, language)


if __name__ == '__main__':
    main()
