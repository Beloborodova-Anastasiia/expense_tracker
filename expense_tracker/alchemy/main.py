# from datetime import date, time, datetime
# from csv import DictReader
# from utils import (compute_summary, create_database, create_session,
#                    extract_categories, get_or_create, load_transactions,
#                    compute_category_summary)
import utils
from models import Summary, Transaction
from sqlalchemy import select
from sqlalchemy.sql import func


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
    data_transactions = 'data/MonzoDataExport_July_2022-08-19_202128.csv'
    utils.load_transactions(session, data_transactions)
    data_transactions = 'data/MonzoDataExport_August_2022-09-01_091402.csv'
    utils.load_transactions(session, data_transactions)
    # transaction = get_or_create(
    #     session,
    #     Transaction,
    #     name='XXX',
    #     type='DDD',
    #     category='DDD',
    # )
    # print(transaction)

    # session.add_all([first, second])
    # session.commit()
    # database.handle('MonzoDataExport_July_2022-08-19_202128.csv')
    # handle()
    # instance = session.query(func.avg(Transactions.amount)).filter_by(category='Bills')
    # print(Transactions.__table__)
    # 
    # trans = select(Transaction).where(Transaction.category.in_(['Expenses']))
    # for user in session.scalars(trans):
    #     print(user)
    categories = utils.extract_categories(session)
    # print(categories)
    spending = {}

    income, outcome, remainder = utils.compute_summary(session, '2022-08')
    for category in categories:
        if category not in utils.UNACCOUNTED_CATEGORIES:
            spending[category] = utils.compute_category_summary(
                session, '2022-07', category
            )
    # print(income, outcome, remainder)
    utils.load_spendings(session, '2022-07')    


if __name__ == '__main__':
    main()
