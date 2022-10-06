from csv import DictReader
from datetime import datetime
from sre_constants import IN_LOC_IGNORE

from models import Spending, Transaction
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

UNACCOUNTED_CATEGORIES = ['Transfers', 'Family']
INCOM_CATEGORIES = ['Income']


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def create_database(db_path, model):
    db_engine = create_engine(db_path)
    # Base.metadata.create_all(engine)
    model.metadata.create_all(db_engine)
    return db_engine


def create_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    return session


def load_transactions(session, file):
    for row in DictReader(open(file)):
        get_or_create(
            session,
            Transaction,
            transaction_id=row['Transaction ID'],
            name=row['Name'],
            type=row['Type'],
            category=row['Category'],
            date=datetime.strptime(row['Date'], '%d/%m/%Y').date(),
            time=datetime.strptime(row['Time'], '%H:%M:%S').time(),
            amount=row['Amount'],
            local_currency=row['Local currency'],
            notes=row['Notes and #tags'],
            address=row['Address'],
            description=row['Description'],
        )


def compute_summary(session, date):

    transactions = select(Transaction).filter(
        Transaction.date.like(f'%{date}%')
    ).where(Transaction.category.notin_(UNACCOUNTED_CATEGORIES))
    remainder = 0
    for trans in session.scalars(transactions):
        remainder += trans.amount
    remainder = round(remainder, 2)

    income = 0
    incoming = select(Transaction).filter(
        Transaction.date.like(f'%{date}%')
    ).where(Transaction.category.in_(INCOM_CATEGORIES))
    for trans in session.scalars(incoming):
        income += trans.amount
        income = round(income, 2)

    outcome = 0
    outcoming = select(Transaction).filter(
        Transaction.date.like(f'%{date}%')
    ).where(Transaction.category.notin_(
        INCOM_CATEGORIES + UNACCOUNTED_CATEGORIES
    ))
    for trans in session.scalars(outcoming):
        outcome += trans.amount
        outcome = round(outcome, 2)

    return income, outcome, remainder


def extract_categories(session):
    categorys = []
    transactions = session.query(Transaction)
    for transaction in session.scalars(transactions):
        if transaction.category not in categorys:
            categorys.append(transaction.category)
    return categorys


def compute_category_summary(session, date, category):
    transactions = select(Transaction).filter(
        Transaction.date.like(f'%{date}%')
    ).where(Transaction.category.in_([category]))
    sum = 0
    for trans in session.scalars(transactions):
        sum += trans.amount
    return round(sum, 2)


def compute_spendings(session, date):
    categories = extract_categories(session)
    spending = {}
    for category in categories:
        if category not in UNACCOUNTED_CATEGORIES:
            spending[category] = compute_category_summary(
                session, date, category
            )
    return spending


def load_spendings(session, date):
    spendings = compute_spendings(session, date)
    for spending in spendings.keys():
        print(spending, spendings[spending])
    # get_or_create(
    #         session,
    #         Spending,
    #         month = date,
    #         caregory = 
