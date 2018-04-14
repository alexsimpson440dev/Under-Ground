from src.database import Database
from src.models.table_user import User


class Select(object):
    def __init__(self):
        self.DB = Database()

    def _get_session(self):
        session = self.DB.get_session()
        return session

    def select_email(self, email_address):
        session = self._get_session()
        for user in session.query(User.email_address).filter(User.email_address==email_address):
            print(user.email_address)