from sqlalchemy import Column, Integer, Date, Float, Sequence, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from src.database import Base


class UserInfo(Base):

    __tablename__ = 'user_info'

    info_id = Column(Integer, Sequence('article_aid_seq', start=1, increment=1, optional=True), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    account_id = Column(Integer, ForeignKey('bill_account.account_id'))
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String(2))
    zip = Column(Integer)
    phone = Column(String(12))

    users = relationship("User", backref=backref("user_info", uselist=False))
    bill_accounts = relationship("BillAccount", backref="user_info")

    def __init__(self, first_name, last_name, address, city, state, zip, phone, users, bill_accounts, info_id=None):
        self.info_id = info_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone = phone
        # relationships
        self.users = users
        self.bill_accounts = bill_accounts
