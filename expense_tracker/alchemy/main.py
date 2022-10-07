# from datetime import date, time, datetime
# from csv import DictReader
# from utils import (compute_summary, create_database, create_session,
#                    extract_categories, get_or_create, load_transactions,
#                    compute_category_summary)
import utils
from models import Summary, Transaction
from sqlalchemy import select
from sqlalchemy.sql import func
from csv import DictReader


def main():
    engine = utils.create_database('sqlite:///tranasactions.db', Transaction)
    # engine = create_database('sqlite:///tranasactions.db', Summary)
    # while True:
    #     try:
    #         data_transactions = input('Enter path to file: \n')
    #         # func = getattr(command, command[0])
    #         load_transactions(data_transactions, engine)
    #     except FileNotFoundError:
    #         print('File not found')
    #     else:
    #         break
    session = utils.create_session(engine)
    # data_transactions = input()
    data_transactions = 'data/Nastia.csv'
    utils.load_transactions(session, data_transactions, 'Nastia')
    data_transactions = 'data/Alex.csv'
    utils.load_transactions(session, data_transactions, 'Alex')
    dates = utils.extract_dates(data_transactions)
    for date in dates:
        utils.load_spendings(session, date)
        utils.load_summary(session, date)
        utils.compute_accumulation(session)
    utils.compute_average(session)


if __name__ == '__main__':
    main()
