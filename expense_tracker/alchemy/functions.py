from csv import DictReader
from datetime import datetime

from models import Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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


def load_transactions(file, session):
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
