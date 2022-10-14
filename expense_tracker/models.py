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
    month = Column(Integer)
    year = Column(Integer)
    income = Column(Float)
    outcome = Column(Float)
    remainder = Column(Float)

    def __repr__(self):
        return (
            f'<Summary(month={self.month}, '
            f'income={self.income}), '
            f'outcome={self.outcome}, '
            f'remainder={self.remainder}>'
        )


class Spending(Base):
    __tablename__ = 'spending'

    id = Column(Integer, primary_key=True)
    month = Column(Integer)
    year = Column(Integer)
    category = Column(String)
    spending = Column(Float)

    def __repr__(self):
        return (
            f'<Spending(month={self.month}, '
            f'category={self.category}), '
            f'spending={self.spending}>'
        )


class Accumulation(Base):
    __tablename__ = 'accumulation'

    id = Column(Integer, primary_key=True)
    revenue = Column(Integer)
    spending = Column(Integer)
    accumulation = Column(Integer)

    def __repr__(self):
        return (
            f'<Accumulation(revenue={self.revenue}, '
            f'spending={self.spending}), '
            f'accumulation={self.accumulation}>'
        )


class Average(Base):
    __tablename__ = 'average'

    id = Column(Integer, primary_key=True)
    category = Column(String)
    spending = Column(Float)

    def __repr__(self):
        return (
            f'<Average(category={self.category}, '
            f'spending={self.spending}>'
        )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    relative = Column(String)

    def __repr__(self):
        return (
            f'<User(username={self.name}, '
            f'relative={self.relative}>'
        )
