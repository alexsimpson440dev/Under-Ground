from src.queries.insert import Insert
from src.models.table_user import User

insert = Insert()
class QueryManager(object):
    def __init__(self):
        pass

    def insert_user(self, username, email, password):
        user = User(username, email, password)
        insert.insert_object(user)