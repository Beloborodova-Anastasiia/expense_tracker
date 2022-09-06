from sqlalchemy import Column, Date, Float, Integer, String, Time
from sqlalchemy.orm import declarative_base


class TransactionModel():
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
        return (f'<Transaction(name={self.name}, '
                f'date={self.date}, '
                f'amount={self.amount})>'
        )