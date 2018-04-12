from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

class Insert(object):
    def __init__(self, connection_string='sqlite:///test.sqlite3'):
        self.db = connection_string
        self.engine = create_engine(self.db, convert_unicode=True)
        self.meta = MetaData()

    def insert_object(self, object):
        Session = sessionmaker()
        conn = self.engine.connect()
        session = Session(bind=conn)
        session.add(object)
        session.commit()
        session.close()