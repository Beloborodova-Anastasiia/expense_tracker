from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Date, Float, Integer, String, Time
from sqlalchemy.orm import sessionmaker
from datetime import date, time, datetime
from csv import DictReader
from sqlalchemy.sql import func
from sqlalchemy import select

from models import TransactionModel
from moduls import get_or_create_base


Base = declarative_base()


class Transactions(Base, TransactionModel):
    pass


class Database:
    def __init__(self, database):
        self.engine = create_engine(database)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def handle(self, file):
        for row in DictReader(open(file)):
            get_or_create_base(
                self.session,
                Transactions,
                transaction_id = row['Transaction ID'],
                name = row['Name'],
                type = row['Type'],
                category = row['Category'],
                date = datetime.strptime(row['Date'], '%d/%m/%Y').date(),
                time = datetime.strptime(row['Time'], '%H:%M:%S').time(),
                amount = row['Amount'],
                local_currency = row['Local currency'],
                notes = row['Notes and #tags'],
                address = row['Address'],
                description = row['Description'],
            )


def main():
    
    database = Database('sqlite:///tranasactions.db')
    first = Transactions(
        transaction_id = 1,
        name = 'first',
        type = 'f',
        category = 'xxxx',
        amount = 324.3,
    )
    second = Transactions(
        transaction_id = 1,
        name = 'second',
        type = 's',
        category = 'xxxx',
        amount = 324.3,
    )
    database.session.add_all([first, second])
    database.session.commit()
    # database.handle('expense_tracker/alchemy/MonzoDataExport_July_2022-08-19_202128.csv')
    # handle()
    # instance = session.query(func.avg(Transactions.amount)).filter_by(category='Bills')
    # print(Transactions.__table__)
    trans = select(Transactions).where(Transactions.name.in_(['first']))
    for user in database.session.scalars(trans):
        print(user)


if __name__ == '__main__':
    main()