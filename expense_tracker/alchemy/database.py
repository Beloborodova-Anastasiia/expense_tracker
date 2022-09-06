from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Date, Float, Integer, String, Time
from sqlalchemy.orm import sessionmaker
from datetime import date, time, datetime
from csv import DictReader
from sqlalchemy.sql import func

from models import Transaction
from moduls import get_or_create_base

engine = create_engine('sqlite:///tranasactions.db')
Base = declarative_base()


class Transaction_base(Base, Transaction):
    pass


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def handle():

        for row in DictReader(open('expense_tracker/alchemy/MonzoDataExport_July_2022-08-19_202128.csv')):
            
            get_or_create_base(
                session,
                Transaction,
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

