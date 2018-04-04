from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from src.database import Database

db = Database()

class Insert(object):
    def __init__(self, connection_string='sqlite:///test.sqlite3'):
        self.db = connection_string
        self.engine = db.engine

    def _get_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    def insert_object(self, object):
        session = self._get_session()
        session.add(object)
        session.commit()
        session.close()