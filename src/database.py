from sqlalchemy import Table, MetaData, Column, Integer, Float, String, Date, ForeignKey, create_engine
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.schema import Sequence

from src.models.table_user import User
from src.models.table_user_info import UserInfo
from src.models.table_manager import Manager
from src.models.table_bill_account import BillAccount
from src.models.table_bill_config import BillConfig
from src.models.table_bill import Bill

METADATA = MetaData()


class Database(object):
    def __init__(self, connection_string='postgres://ddelwwtqhzrqec:7de7df887c166a9eefbf09643d3f9954a6f9a183bc67ced17b515066fa6c7594@ec2-54-235-85-127.compute-1.amazonaws.com:5432/d8fob77u3eb9tn'):
        self.db = connection_string

        self.user = self._map_user()
        self.user_info = self._map_user_info()
        self.manager = self._map_manager()
        self.bill_account = self._map_bill_account()
        self.bill_config = self._map_bill_config()
        self.bill = self._map_bill()

        self.engine = self._create_db()
        METADATA.create_all(bind=self.engine)


    def _create_db(self):
        engine = create_engine(self.db)
        return engine

    def _map_user(self):
        user = Table('user', METADATA,
                     Column('user_id', Integer, Sequence('article_aid_seq', start=1001, increment=1, optional=True), primary_key=True),
                     Column('user_type', Integer),
                     Column('user_name', String(15)),
                     Column('email_address', String(25)),
                     Column('password', String)
                     )
        mapper(User, user,
        properties={'user_info':relationship(UserInfo, backref='user'),
                    'manager':relationship(Manager, backref='user')}
               )
        return user

    def _map_user_info(self):
        user_info = Table('user_info', METADATA,
                      Column('info_id', Integer, Sequence('article_aid_seq', start=1, increment=1, optional=True), primary_key=True),
                      Column('user_id', Integer, ForeignKey('user.user_id')),
                      Column('manager_id', Integer, ForeignKey('manager.manager_id')),
                      Column('account_id', Integer, ForeignKey('bill_account.account_id')),
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

    def _map_bill_account(self):
        bill_account = Table('bill_account', METADATA,
                             Column('account_id', Integer, Sequence('article_aid_seq', start=100001, increment=1, optional=True), primary_key=True),
                             Column('manager_id', Integer, ForeignKey('manager.manager_id')),
                             Column('account_name', String(15)),
                             Column('account_type', Integer)
                             )
        mapper(BillAccount, bill_account,
               properties={'bill_config':relationship(BillConfig, backref='bill_account'),
                           'user_info':relationship(UserInfo, backref='bill_account')}
               )
        return bill_account

    def _map_manager(self):
        manager = Table('manager', METADATA,
                        Column('manager_id', Integer, Sequence('article_aid_seq', start=10001, increment=1, optional=True), primary_key=True),
                        Column('user_id', Integer, ForeignKey('user.user_id'))
                        )
        mapper(Manager, manager,
               properties={'bill_account':relationship(BillAccount, backref='manager'),
                           'user_info':relationship(UserInfo, backref='manager')}
               )
        return manager

    def _map_bill_config(self):
        bill_config = Table('bill_config', METADATA,
                            Column('bill_config_id', Integer, Sequence('article_aid_seq', start=1, increment=1, optional=True), primary_key=True),
                            Column('account_id', Integer, ForeignKey('bill_account.account_id')),
                            Column('bill_1', String(10)),
                            Column('bill_2', String(10)),
                            Column('bill_3', String(10)),
                            Column('bill_4', String(10)),
                            Column('bill_5', String(10))
                            )
        mapper(BillConfig, bill_config,
               properties={'bill': relationship(Bill, backref='bill_config')}
               )
        return bill_config

    def _map_bill(self):
        bill = Table('bill', METADATA,
                     Column('bill_id', Integer, Sequence('article_aid_seq', start=50001, increment=1, optional=True), primary_key=True),
                     Column('bill_config_id', Integer, ForeignKey('bill_config.bill_config_id')),
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
