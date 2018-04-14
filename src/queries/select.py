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
        for user in session.query(User.email_address).filter(User.email_address==email_address):
            return user.email_address

    def select_user_name(self, user_name):
        session = self._get_session()
        for user in session.query(User.user_name).filter(User.user_name==user_name):
            return user.user_name