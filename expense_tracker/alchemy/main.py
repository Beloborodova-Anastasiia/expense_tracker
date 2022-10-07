# from datetime import date, time, datetime
# from csv import DictReader
# from utils import (compute_summary, create_database, create_session,
#                    extract_categories, get_or_create, load_transactions,
#                    compute_category_summary)
# from utils import TRANSACTIONS_AUTHORS
import utils
from models import Transaction
# from sqlalchemy import select
# from sqlalchemy.sql import func
# from csv import DictReader

PATH = 'data/'


def main():
    while True:
        transactions_author = input('Enter name transactions authos: \n')
        if transactions_author not in utils.TRANSACTIONS_AUTHORS.keys():
            print('This user is not in the list')
        else:
            break
    engine = utils.create_database('sqlite:///tranasactions.db', Transaction)
    session = utils.create_session(engine)
    while True:
        try:
            file_name = input('Enter file name: \n')
            data_transactions = PATH + file_name
            utils.load_transactions(
                session,
                data_transactions,
                transactions_author
            )
        except FileNotFoundError:
            print('File not found')
        else:
            break

    # data_transactions = input()
    # data_transactions = 'data/Nastia.csv'
    # utils.load_transactions(session, data_transactions, 'Nastia')
    # data_transactions = 'data/Alex.csv'
    # utils.load_transactions(session, data_transactions, 'Alex')
    dates = utils.extract_dates(data_transactions)
    for date in dates:
        utils.load_spendings(session, date)
        utils.load_summary(session, date)
    utils.compute_accumulation(session)
    utils.compute_average(session)


if __name__ == '__main__':
    main()
