from sqlalchemy import Column, Integer, Date, Float, Sequence, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from src.database import Base

class BillConfig(Base):

    __tablename__ = 'bill_config'

    bill_config_id = Column(Integer, Sequence('article_aid_seq', start=1, increment=1, optional=True), primary_key=True)
    account_id = Column(Integer, ForeignKey('bill_account.account_id'))
    bill_1 = Column(String(10))
    bill_2 = Column(String(10))
    bill_3 = Column(String(10))
    bill_4 = Column(String(10))
    bill_5 = Column(String(10))

    bill_accounts = relationship("BillAccount", backref=backref("bill_config", uselist=False))

    def __init__(self, bill_1, bill_2, bill_3, bill_4, bill_5, bill_accounts, bill_config_id=None):
        self.bill_config_id = bill_config_id
        self.bill_1 = bill_1
        self.bill_2 = bill_2
        self.bill_3 = bill_3
        self.bill_4 = bill_4
        self.bill_5 = bill_5
        # relationships
        self.bill_accounts = bill_accounts