from src.database import Database


class Insert(object):
    def __init__(self):
        self.DB = Database()

    def insert_object(self, object):
        session = self.DB.session
        session.add(object)
        session.commit()
        session.close()
