from sqlalchemy import create_engine, engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from src.models.table_user import User

metadata = MetaData()

class Select(object):
    def __init__(self):
        metadata.create_all(bind="sqlite:///test.sqlite3")

    def _get_session(self):
        session = Session()
        return session

    def select_email(self, email_address):
        session = self._get_session()
        user = session.query(User).filter(User.email_address == email_address):

