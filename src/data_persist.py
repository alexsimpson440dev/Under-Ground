from src.query_manager import QueryManager

from src.models.table_user import User
from src.models.table_user_info import UserInfo
from src.models.table_manager import Manager

import bcrypt

query = QueryManager()


class DataPersist(object):
    def __init__(self):
        pass

    def persist_user(self, new_user, manager_id):
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
        phone = new_user.get('phone_number')
        account = query.select_bill_account(manager_id)
        user_info = UserInfo(first_name, last_name, address, city, state, zip, phone, user, account)

        query.insert_data(user)
        query.insert_data(user_info)

    def persist_manager(self, new_manager):
            user_name = new_manager.get('user_name')
            email_address = new_manager.get('email_address')
            password = new_manager.get('password1')
            hashed_password = self._hash_password(password.encode('utf-8'))
            user = User(user_name, email_address, hashed_password)

            query.insert_data(user)
            self._persist_manager(user)
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # todo: add manager with userID
            # todo: add bill account
            # todo: add user info

    @staticmethod
    def _persist_manager(user):
        manager = Manager(user)

        query.insert_data(manager)

    # encrypts password
    @staticmethod
    def _hash_password(password):
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        hashed_password = hashed_password.decode('utf-8')

        return hashed_password
