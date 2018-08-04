import bcrypt

from src.managers.session_manager import SessionManager
from src.managers.query_manager import QueryManager
from src.models.table_manager import Manager
from src.models.table_user import User
from src.models.table_user_info import UserInfo
from src.models.table_bill_account import BillAccount
from src.models.table_bill_config import BillConfig

query = QueryManager()
web_session = SessionManager()


class DataPersist(object):
    def __init__(self):
        pass

    def persist_user(self, new_user, manager_id):
        user_name = new_user.get('user_name')
        email_address = new_user.get('email_address')
        password = new_user.get('password1')
        hashed_password = self._hash_password(password.encode('utf-8'))
        user = User(user_name, email_address, hashed_password)
        user_info = self._persist_user_info(new_user, user, manager_id)

        query.insert(user)
        query.insert(user_info)
        query.session_commit()
        query.session_close()

        web_session.set_session('email', email_address)

    @staticmethod
    def _persist_user_info(new_info, user, manager_id):
        if manager_id is None:
            account = None

        else:
            # selects bill account and manager based on the managerID provided
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

            web_session.set_session('email', email_address)

    def persist_bill_account(self, account, email):
        account_name = account.get('account_name')
        account_type = 1
        user = query.select_email(email)
        user_id = user.user_id
        manager = query.select_manager_uid(user_id)

        bill_account = BillAccount(account_name, account_type, manager)
        bill_config = self._persist_bill_config(account, bill_account)

        query.insert(bill_account)
        query.insert(bill_config)
        query.session_commit()
        query.session_close()

        web_session.clear_session('token')

    @staticmethod
    def _persist_bill_config(account, bill_account):
        bill_1 = account.get('bill_1')
        bill_2 = account.get('bill_2')
        bill_3 = account.get('bill_3')
        bill_4 = account.get('bill_4')
        bill_5 = account.get('bill_5')
        bill_config = BillConfig(bill_1, bill_2, bill_3, bill_4, bill_5, bill_account)

        return bill_config

    # encrypts password
    @staticmethod
    def _hash_password(password):
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        hashed_password = hashed_password.decode('utf-8')

        return hashed_password

    @staticmethod
    def logger(message):
        print(message)
