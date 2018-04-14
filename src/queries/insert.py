from src.database import Database


class Insert(object):
    def __init__(self):
        self.DB = Database()

    def _session(self):
        session = self.DB.get_session()
        return session

    def insert_object(self, object):
        session = self._session()
        session.add(object)
        session.commit()
        session.close()
