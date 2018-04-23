from src.query_manager import QueryManager

from src.models.table_user import User
from src.models.table_user_info import UserInfo

import bcrypt

query = QueryManager()

class DataPersister(object):
    def __init__(self):
        pass

    def persist_user(self, new_user):
        user_name = new_user.get('user_name')
        email_address = new_user.get('email_address')
        password = new_user.get('password1')
        hashed_password = self._hash_password(password.encode('utf-8'))
        user = User(user_name, email_address, hashed_password)

        first_name = new_user.get('first_name')
        last_name = new_user.get('last_name')
        address = new_user.get('address')
        city = new_user.get('city')
        state = new_user.get('state')
        zip = new_user.get('zip')
        phone = new_user.get('phone')
        manager = query.select_manager()


        query.insert_user(user)

    # encrypts password
    @staticmethod
    def _hash_password(password):
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        hashed_password = hashed_password.decode('utf-8')

        return hashed_password
