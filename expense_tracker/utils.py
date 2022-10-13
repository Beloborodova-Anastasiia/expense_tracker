from csv import DictReader
from datetime import datetime

from models import Accumulation, Average, Spending, Summary, Transaction, User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, functions

CATEGORY_FAMILY = 'Family'
UNACCOUNTED_CATEGORIES = [CATEGORY_FAMILY, ]
UNACCOUNTED_TYPES = ['Pot transfer', ]
INCOM_CATEGORIES = ['Income']
# USERS_RELATIONS = {
#     'Nastia': 'Aleksandr Beloborodov',
#     'Alex': 'Anastasiia Beloborodova'
# }
PATH_TO_DATA = 'data/'


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
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


def load_transactions(session, file, user):
    for row in DictReader(open(file)):
        # if row['Name'] == USERS_RELATIONS[author]:
        if row['Name'] == user.relative:
            category = CATEGORY_FAMILY
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
            if transaction.category not in UNACCOUNTED_CATEGORIES:
                categorys.append(transaction.category)
    return categorys


def compute_category_summary(session, date, category):
    transactions = select(Transaction).filter(
        Transaction.date.like(f'%{date}%')
    ).where(Transaction.category.in_([category])).where(
        Transaction.type.notin_(UNACCOUNTED_TYPES)
    )
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
        if spendings[spending] != 0:
            year, month = date.split('-')
            spending_category = get_or_create(
                session,
                Spending,
                month=month,
                year=year,
                category=spending,
            )
            spending_category.spending = abs(spendings[spending])
            session.commit()


def load_summary(session, date):
    income, outcome, remainder = compute_summary(session, date)
    year, month = date.split('-')
    summary = get_or_create(
        session,
        Summary,
        year=year,
        month=month,
    )
    summary.income = income
    summary.outcome = outcome
    summary.remainder = remainder
    session.commit()


def compute_accumulation(session):
    accumulation = session.query(functions.sum(Summary.remainder)).scalar()
    revenue = session.query(functions.sum(Summary.income)).scalar()
    spending = session.query(functions.sum(Summary.outcome)).scalar()
    total = get_or_create(
            session,
            Accumulation,
    )
    total.accumulation = round(accumulation, 2)
    total.revenue = round(revenue, 2)
    total.spending = round(spending, 2)
    session.commit()

    return revenue, spending, accumulation


def compute_average(session):
    categories = extract_categories(session)
    for category in categories:
        average_spendings = session.query(
            func.avg(Spending.spending).label('average')
        ).filter_by(category=category).filter_by(category=category).scalar()
        average_spendings = round(average_spendings, 2)
        average = get_or_create(
            session,
            Average,
            category=category,
        )
        average.spending = average_spendings
        session.commit()


def handle_transactions_file(username=None, file=None):
    engine = create_database('sqlite:///tranasactions.db', Transaction)
    session = create_session(engine)
    if not username:
        username = input('Enter name transactions authos: \n')
    user = get_or_create(
        session,
        User,
        username=username
    )
    if not user.relative:
        relative = input('Enter full name relative: \n')
    # if user not in USERS_RELATIONS.keys():
        # print('This user is not in the list')
        user.relative = relative

    if not file:
        while True:
            try:
                file_name = input('Enter file name: \n')
                data_transactions = PATH_TO_DATA + file_name
                load_transactions(
                    session,
                    data_transactions,
                    user
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
    dates = extract_dates(data_transactions)
    for date in dates:
        load_spendings(session, date)
        load_summary(session, date)
    compute_accumulation(session)
    compute_average(session)
