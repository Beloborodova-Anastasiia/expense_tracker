from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Date, Float, Integer, String, Time
from sqlalchemy.orm import sessionmaker
from datetime import date, time, datetime
from csv import DictReader
from sqlalchemy.sql import func


engine = create_engine('sqlite:///tranasactions.db')
Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String)
    name = Column(String)
    type = Column(String)
    category = Column(String)
    date = Column(Date)
    time = Column(Time)
    amount = Column(Float)
    local_currency = Column(String)
    notes = Column(String)
    address = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<Transaction(name='%s', date='%s', amount='%s')>" % (
                            self.name, self.date, self.amount)



Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def handle():

        for row in DictReader(open('MonzoDataExport_July_2022-08-19_202128.csv')):
            
            # date = datetime.strptime(row['Date'], '%d/%m/%Y')
            get_or_create(
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

def main():
    
    handle()
    instance = session.query(func.avg(Transaction.amount)).filter_by(category='Bills')
    print(Transaction.__table__)

if __name__ == '__main__':
    main()