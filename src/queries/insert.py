from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Database

class Insert(object):
    def __init__(self, connection_string='postgres://ddelwwtqhzrqec:7de7df887c166a9eefbf09643d3f9954a6f9a183bc67ced17b515066fa6c7594@ec2-54-235-85-127.compute-1.amazonaws.com:5432/d8fob77u3eb9tn'):
        self.db = connection_string
        self.engine = create_engine(self.db)

    def _get_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    def insert_object(self, object):
        session = self._get_session()
        session.add(object)
        session.commit()
        session.close()