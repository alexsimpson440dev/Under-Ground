from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper

metadata = MetaData()

user = Table('user', metadata,
             Column('UserID', Integer, primary_key=True),
             Column('UserType', String),
             Column('UserName', String),
             Column('EmailAddress', String),
             Column('Password', String)
             )

class User(object):
    def __init__(self, user_type, username, email_address, password):
        self.UserType = user_type
        self.UserName = username
        self.EmailAddress = email_address
        self.Password = password


mapper(User, user)
