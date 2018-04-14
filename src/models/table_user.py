from sqlalchemy import Column, Integer, Date, Float, Sequence, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from src.database import Base


class User(Base):

    __tablename__ = 'user'

    user_id = Column(Integer, Sequence('article_aid_seq', start=1001, increment=1, optional=True), primary_key=True)
    user_type = Column(Integer)
    user_name = Column(String(15))
    email_address = Column(String(25))
    password = Column('password', String)

    def __init__(self, username, email_address, password, user_id=None, user_type=3):
        self.user_id = user_id
        self.user_type = user_type
        self.user_name = username
        self.email_address = email_address
        self.password = password
