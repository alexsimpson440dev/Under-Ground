import bcrypt

from src.managers.query_manager import QueryManager
from src.models.table_manager import Manager
from src.models.table_user import User
from src.models.table_user_info import UserInfo

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
        user_info = self._persist_user_info(new_user, manager_id, user)

        query.insert(user)
        query.insert(user_info)
        query.session_commit()
        query.session_close()

    @staticmethod
    def _persist_user_info(new_info, user, manager_id):
        if manager_id is None:
            account = None
        else:
            print('id: ' + manager_id)
            account = query.select_bill_account(manager_id)

        first_name = new_info.get('first_name')
        last_name = new_info.get('last_name')
        address = new_info.get('address')
        city = new_info.get('city')
        state = new_info.get('state')
        zip_code = new_info.get('zip')
        phone = new_info.get('phone_number')
        user_info = UserInfo(first_name, last_name, address, city, state, zip_code, phone, user, account)

        return user_info

    def persist_manager(self, new_manager):
            user_name = new_manager.get('user_name')
            email_address = new_manager.get('email_address')
            password = new_manager.get('password1')
            hashed_password = self._hash_password(password.encode('utf-8'))

            user = User(user_name, email_address, hashed_password, user_type=1)
            manager = Manager(user)
            user_info = self._persist_user_info(new_manager, user, manager_id=None)

            query.insert(user)
            query.insert(manager)
            query.insert(user_info)
            query.session_commit()
            query.session_close()
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # todo: add manager with userID
            # todo: add bill account

    # encrypts password
    @staticmethod
    def _hash_password(password):
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        hashed_password = hashed_password.decode('utf-8')

        return hashed_password
