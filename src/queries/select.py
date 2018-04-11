from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Database



class Select(object):
    def __init__(self, connection_string='postgres://ddelwwtqhzrqec:7de7df887c166a9eefbf09643d3f9954a6f9a183bc67ced17b515066fa6c7594@ec2-54-235-85-127.compute-1.amazonaws.com:5432/d8fob77u3eb9tn'):
        self.db = connection_string
        self.engine = create_engine(self.db)

    def _get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session

    def select_email(self, email_address):
        Session = self._get_session()
        conn = self.engine.connect()
        session = Session(bind=conn)
        for email, in session.query(User).filter(User.email_address==email_address):
            print(email)