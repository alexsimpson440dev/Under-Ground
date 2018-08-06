from sqlalchemy import Column, Integer, Date, Float, Sequence, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref
from src.database import Base


class Paid(Base):

    __tablename__ = 'paid'

    paid_id = Column(Integer, Sequence('article_aid_seq', start=50001, increment=1, optional=True), primary_key=True)
    bill_id = Column(Integer, ForeignKey('bill.bill_id'))
    user_id = Column(Integer)
    paid = Column(Boolean)
    date_paid = Column(Date)

    bills = relationship("Bill", backref=backref("paid", uselist=False))

    def __init__(self, user_id, bills, paid=False, date_paid=None, paid_id=None):
        self.paid_id = paid_id
        self.user_id = user_id
        self.paid = paid
        self.date_paid = date_paid
        # relationships
        self.bills = bills
