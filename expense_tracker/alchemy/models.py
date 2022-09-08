from sqlalchemy import Column, Date, Float, Integer, String, Time
from sqlalchemy.orm import declarative_base

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
        return (
            f'<Transaction(name={self.name}, '
            f'date={self.date}, '
            f'amount={self.amount})>'
        )


class Summary(Base):
    __tablename__ = 'summary'

    id = Column(Integer, primary_key=True)
    month = Column(Date)
    income = Column(Float)
    outcome = Column(Float)
    bills = Column(Float)
    transport = Column(Float)
    groseries = Column(Float)
    shopping = Column(Float)
    eating_out = Column(Float)
    entertainment = Column(Float)
    holidays = Column(Float)
    others = Column(Float)

    def __repr__(self):
        return (
            f'<Summary(month={self.month}, '
            f'income={self.income}), '
            f'outcome={self.outcome}>'
        )
