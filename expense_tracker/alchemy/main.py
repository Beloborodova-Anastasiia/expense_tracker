# from datetime import date, time, datetime
# from csv import DictReader
from sqlalchemy.sql import func
from sqlalchemy import select
from models import Transaction, Summary

from functions import (create_database, create_session,
                       get_or_create, load_transactions)


def main():
    engine = create_database('sqlite:///tranasactions.db', Transaction)
    engine = create_database('sqlite:///tranasactions.db', Summary)
    # while True:
    #     try:
    #         data_transactions = input('Enter path to file: \n')
    #         # func = getattr(command, command[0])
    #         load_transactions(data_transactions, engine)
    #     except FileNotFoundError:
    #         print('File not found')
    #     else:
    #         break
    session = create_session(engine)
    # data_transactions = input()
    data_transactions = 'data/MonzoDataExport_July_2022-08-19_202128.csv'
    load_transactions(data_transactions, session)
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
    # categorys = []
    # trans = session.query(Transaction)
    # for transaction in session.scalars(trans):
    #     if transaction.category not in categorys:
    #         categorys.append(transaction.category)
    # print(categorys)
    # trans = select(Transaction).where(Transaction.category.in_(['Expenses']))
    # for user in session.scalars(trans):
    #     print(user)

if __name__ == '__main__':
    main()
