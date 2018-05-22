from sqlalchemy import Column, Integer, Date, Float, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from src.database import Base


class Manager(Base):

    __tablename__ = 'manager'

    manager_id = Column(Integer, Sequence('article_aid_seq', start=10001, increment=1, optional=True), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    users = relationship("User", backref=backref("manager", uselist=False))

    def __init__(self, users, manager_id=None):
        self.manager_id = manager_id
        # relationships
        self.users = users
