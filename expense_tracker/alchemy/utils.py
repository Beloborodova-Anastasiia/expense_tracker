from csv import DictReader
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.sql import functions

from models import Accumulation, Spending, Summary, Transaction
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

UNACCOUNTED_CATEGORIES = ['Family', ]
UNACCOUNTED_TYPES = ['Pot transfer', ]
INCOM_CATEGORIES = ['Income']
SPOUSE = {
    'Nastia': 'Aleksandr Beloborodov',
    'Alex': 'Anastasiia Beloborodova'
}


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


def load_transactions(session, file, author):
    for row in DictReader(open(file)):
        if row['Name'] == SPOUSE[author]:
            category = 'Family'
        else:
            category = row['Category']
        get_or_create(
            session,
            Transaction,
            transaction_id=row['Transaction ID'],
            name=row['Name'],
            type=row['Type'],
            category=category,
            date=datetime.strptime(row['Date'], '%d/%m/%Y').date(),
            time=datetime.strptime(row['Time'], '%H:%M:%S').time(),
            amount=row['Amount'],
            local_currency=row['Local currency'],
            notes=row['Notes and #tags'],
            address=row['Address'],
            description=row['Description'],
        )


def extract_dates(file):
    dates = []
    for row in DictReader(open(file)):
        date = '{:%Y-%m}'.format(datetime.strptime(row['Date'], '%d/%m/%Y'))
        if date not in dates:
            dates.append(date)
    return dates


def compute_summary(session, date):

    transactions = select(Transaction).filter(
        Transaction.date.like(f'%{date}%')
    ).where(Transaction.category.notin_(UNACCOUNTED_CATEGORIES)).where(
        Transaction.type.notin_(UNACCOUNTED_TYPES)
        )
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
    )).where(
        Transaction.type.notin_(UNACCOUNTED_TYPES)
        )
    for trans in session.scalars(outcoming):
        outcome += trans.amount
        outcome = round(outcome, 2)

    return income, abs(outcome), remainder


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
        if category not in UNACCOUNTED_CATEGORIES + INCOM_CATEGORIES:
            spending[category] = compute_category_summary(
                session, date, category
            )
    return spending


def load_spendings(session, date):
    spendings = compute_spendings(session, date)
    for spending in spendings.keys():
        if spendings[spending] != 0:
            year, month = date.split('-')
            get_or_create(
                session,
                Spending,
                month=month,
                year=year,
                category=spending,
                spending=abs(spendings[spending])
            )


def load_summary(session, date):
    income, outcome, remainder = compute_summary(session, date)
    year, month = date.split('-')
    get_or_create(
        session,
        Summary,
        year=year,
        month=month,
        income=income,
        outcome=outcome,
        remainder=remainder,
    )


def compute_accumulation(session):
    accumulation = session.query(functions.sum(Summary.remainder)).scalar()
    revenue = session.query(functions.sum(Summary.income)).scalar()
    spending = session.query(functions.sum(Summary.outcome)).scalar()
    total = session.query(Accumulation).first()
    if total:
        total.accumulation = round(accumulation, 2)
        total.revenue = round(revenue, 2)
        total.spending = round(spending, 2)
        session.commit()
    else:
        get_or_create(
            session,
            Accumulation,
            accumulation=accumulation,
            revenue=revenue,
            spending=spending
        )
    return revenue, spending, accumulation


def compute_average(session):
    categories = extract_categories(session)
    for category in categories:
        average = session.query(
            func.avg(Spending.spending).label('average')
        ).filter_by(category=category).scalar()
        # speding = category_spend.query(
        #     func.avg(Spending.spending).label('average')
        # ).scalar()

        print(average)

