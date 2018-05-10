from src.models import User, UserInfo, Manager, Bill, BillConfig, BillAccount
from src.database import Database


class Select(object):
    def __init__(self):
        self.DB = Database()

    def _get_session(self):
        session = self.DB.get_session()
        return session

    def select_email(self, email_address):
        session = self._get_session()
        for user in session.query(User.email_address).filter(User.email_address == email_address):
            return user.email_address

    def select_user_name(self, user_name):
        session = self._get_session()
        for user in session.query(User.user_name).filter(User.user_name == user_name):
            return user.user_name

    def select_bill_account(self, manager_id):
        session = self._get_session()
        for account in session.query(BillAccount).filter(BillAccount.manager_id == manager_id):
            return account

    def select_manager_object(self, manager_id):
        session = self._get_session()
        for manager in session.query(Manager).filter(Manager.manager_id == manager_id):
            return manager

    def select_user_id(self, email_address):
        session = self._get_session()
        for user in session.query(User.email_address).filter(User.email_address == email_address):
            return user.user_id
