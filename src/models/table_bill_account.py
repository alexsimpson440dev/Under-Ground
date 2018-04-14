from sqlalchemy import Column, Integer, Date, Float, Sequence, ForeignKey, String
from sqlalchemy.orm import relationship
from src.database import Base


class BillAccount(Base):

    __tablename__ = 'bill_account'

    account_id = Column(Integer, Sequence('article_aid_seq', start=100001, increment=1, optional=True), primary_key=True)
    manager_id = Column(Integer, ForeignKey('manager.manager_id'))
    account_name = Column(String(15))
    account_type = Column(Integer)

    managers = relationship("Manager", backref="bill_account")

    def __init__(self,  account_name, account_type, managers, account_id=None):
        self.account_id = account_id
        self.account_name = account_name
        self.account_type = account_type
        # relationships
        self.managers = managers
