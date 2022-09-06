from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Date, Float, Integer, String, Time
from sqlalchemy.orm import sessionmaker
from datetime import date, time, datetime
from csv import DictReader
from sqlalchemy.sql import func

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

# engine = create_engine('sqlite:///tranasactions.db')
# Base = declarative_base()
# class Transactions(Base, TransactionModel):
#     pass
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()


# def handle():

#         for row in DictReader(open('expense_tracker/alchemy/MonzoDataExport_July_2022-08-19_202128.csv')):
            
#             get_or_create_base(
#                 session,
#                 Transactions,
#                 transaction_id = row['Transaction ID'],
#                 name = row['Name'],
#                 type = row['Type'],
#                 category = row['Category'],
#                 date = datetime.strptime(row['Date'], '%d/%m/%Y').date(),
#                 time = datetime.strptime(row['Time'], '%H:%M:%S').time(),
#                 amount = row['Amount'],
#                 local_currency = row['Local currency'],
#                 notes = row['Notes and #tags'],
#                 address = row['Address'],
#                 description = row['Description'],
#             )

def main():
    
    database = Database('sqlite:///tranasactions.db')
    database.handle('expense_tracker/alchemy/MonzoDataExport_July_2022-08-19_202128.csv')
    # handle()
    # instance = session.query(func.avg(Transactions.amount)).filter_by(category='Bills')
    # print(Transactions.__table__)
    


if __name__ == '__main__':
    main()