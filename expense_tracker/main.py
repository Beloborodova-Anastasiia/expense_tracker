# import sys
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5 import QtGui, QtWidgets, QtCore, Qt
from utils import (create_database, create_session,  handle_transactions_file,
                   import_to_csv)
from models import Accumulation, Average, Spending, Summary, Transaction


def main():
    engine = create_database('sqlite:///tranasactions.db', Transaction)
    session = create_session(engine)
    # handle_transactions_file(session)
    # app = QtWidgets.QApplication(sys.argv)
    # application = App()
    # sys.exit(app.exec_())
    import_to_csv(session, Summary)
    import_to_csv(session, Average)
    import_to_csv(session, Accumulation)
    import_to_csv(session, Spending)


if __name__ == '__main__':
    main()
