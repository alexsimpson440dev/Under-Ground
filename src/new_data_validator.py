import re
import bcrypt

from src.managers.query_manager import QueryManager
from src.managers.session_manager import SessionManager

query = QueryManager()
session = SessionManager()


class NewDataValidator(object):
    def __init__(self):
        pass

    def validate_sign_in(self, credentials):
        email_address = credentials.get('email_address')
        password = credentials.get('password')
        user = query.select_email(email_address)

        if user:
            if self.bcrypt_decrypt(password, user.password):
                self.logger('Log: Credentials are Valid')
                session.set_session('email', email_address)
                return True

        else:
            self.logger('Log: Credentials are not Valid')
            return False

    @staticmethod
    def bcrypt_decrypt(password, hashed_password):

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
        else:
            return False


# -------------------------Sign Up-------------------------
    def validate_user(self, user):
        user_name = user.get('user_name')
        email_address = user.get('email_address')
        password1 = user.get('password1')
        password2 = user.get('password2')

        if user_name != '':
            if self._validate_email(email_address) is True:
                if self._validate_password(password1) is True:
                    if query.select_user_name(user_name) is None:
                        if query.select_email(email_address) is None:
                            if password1 == password2:
                                return True

        else:
            return False

    def validate_user_info(self, user_info):
        zip_code = user_info.get('zip')
        phone_number = user_info.get('phone_number')

        try:
            if int(zip_code) and int(phone_number):
                return True
            else:
                return False

        except ValueError as Error:
            print(Error)
            return False

    def validate_manager_id(self, manager_id):
        manager = query.select_manager(manager_id)

        if manager is None:
            return False
        else:
            return manager

    def validate_manager_token(self, token):
        session_token = session.get_session('token')

        if token == session_token:
            return True
        else:
            return False

    def validate_bill_config(self, config):
        if config.get('bill_1') == '':
            return False
        else:
            return True

    @staticmethod
    def _validate_password(password):
        if re.search(r'[a-z]', password):
            if re.search(r'[0-9]', password):
                if len(password) >= 8:
                    return True

                else:
                    print('log: password not long enough, must be 8 characters long')
                    return False
            else:
                print('log: password must contain a number')
                return False
        else:
            print('log: password must contain a letter')
            return False

    @staticmethod
    def _validate_email(email):
        if re.search(r'.+@.+\.com', email):
            return True

        else:
            print('log: email is not valid')
            return False

    @staticmethod
    def logger(message):
        print(message)
