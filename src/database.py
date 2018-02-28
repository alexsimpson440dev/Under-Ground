from sqlalchemy import Table, MetaData, Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.schema import Sequence

from src.tables.table_user import User
from src.tables.table_user_info import UserInfo
from src.tables.table_manager import Manager
METADATA = MetaData()


class Database(object):
    def __init__(self):
        self.user = self._map_user()

    def _map_user(self):
        user = Table('user', METADATA,
                     Column('user_id', Integer, Sequence('article_aid_seq', start=1001, increment=1, optional=True), primary_key=True),
                     Column('user_type', Integer),
                     Column('user_name', String(15)),
                     Column('email_address', String(25)),
                     Column('password', String)
                     )
        mapper(User, user)
        return user

    def _map_user_info(self):
        user_info = Table('user_info', METADATA,
                      Column('user_id', Integer, ForeignKey('user.user_id')),
                      Column('manager_id', Integer),
                      Column('first_name', String),
                      Column('last_name', String),
                      Column('address', String),
                      Column('city', String),
                      Column('state', String(2)),
                      Column('zip', Integer),
                      Column('phone', String(12))
                      )
        mapper(UserInfo, user_info)
        return user_info

    def _map_manager(self):
        manager = Table('manager', METADATA,
                        Column('manager_id', Integer, Sequence('article_aid_seq', start=10001, increment=1, optional=True)),
                        Column('user_id', Integer)
                        )
        mapper(Manager, manager)
