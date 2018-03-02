from sqlalchemy import Table, MetaData, Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.schema import Sequence

from src.tables.table_user import User
from src.tables.table_user_info import UserInfo
from src.tables.table_manager import Manager
from src.tables.table_bill_account import BillAccount
from src.tables.table_bill_config import BillConfig
from src.tables.table_bill import Bill

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
        return manager

    def _map_bill_account(self):
        bill_account = Table('bill_account', METADATA,
                             Column('account_id', Integer, Sequence('article_aid_seq', start=100001, increment=1, optional=True)),
                             Column('manager_id', Integer),
                             Column('account_name', String(15)),
                             Column('account_type', Integer)
                             )
        mapper(BillAccount, bill_account)
        return bill_account

    def _map_bill_config(self):
        bill_config = Table('bill_config', METADATA,
                            Column('bill_config_id', Integer, Sequence('article_aid_seq', start=1, increment=1, optional=True)),
                            Column('account_id', Integer),
                            Column('bill_1', String(10)),
                            Column('bill_2', String(10)),
                            Column('bill_3', String(10)),
                            Column('bill_4', String(10)),
                            Column('bill_5', String(10))
                            )
        mapper(BillConfig, bill_config)
        return bill_config

    def _map_bill(self):
        bill = Table('bill', METADATA,
                     Column('bill_id', Integer, Sequence('article_aid_seq', start=50001, increment=1, optional=True)),
                     Column('bill_config_id', Integer),
                     Column('date', Date),
                     Column('bill_c_1', Float),
                     Column('bill_c_2', Float),
                     Column('bill_c_3', Float),
                     Column('bill_c_4', Float),
                     Column('bill_c_5', Float),
                     Column('total_pp', Float),
                     Column('total', Float),
                     Column('due_date', Date)
                     )
        mapper(Bill, bill)
        return bill
