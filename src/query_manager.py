from src.queries.insert import Insert
from src.queries.select import Select
from src.models.table_user import User

import bcrypt

insert = Insert()
select = Select()

class QueryManager(object):
    def __init__(self):
        pass

#--------------------SELECT QUERIES--------------------------------------------
    # select email_address
    def select_email_address(self, email_address):
        select.select_email(email_address)

#--------------------INSERT QUERIES--------------------------------------------
    # inserts user
    def insert_user(self, username, email_address, password):
        # hashed_password = self._hash_password(password)

        user = User(username, email_address, password)
        insert.insert_object(user)

#--------------------UPDATE QUERIES--------------------------------------------

#--------------------DELETE QUERIES--------------------------------------------

    # encrypts password
    @staticmethod
    def _hash_password(password):
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        hashed_password = hashed_password.decode('utf-8')

        return hashed_password