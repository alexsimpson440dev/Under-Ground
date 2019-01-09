from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
import os

'''engine = create_engine('sqlite:///test.sqlite3')
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)'''

Base = declarative_base()


class Database(object):
    def __init__(self, connection_string=os.environ['TEST_DATABASE_URL']):
        if 'sqlite' in connection_string:
            self.engine = create_engine(connection_string, poolclass=NullPool, connect_args={'check_same_thread': False})

        else:
            self.engine = create_engine(connection_string, poolclass=NullPool)

        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.session = self.Session()
