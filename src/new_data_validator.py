import re
import bcrypt
import numbers
from datetime import datetime

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

        if user_name != '' \
            and self._validate_email(email_address)\
            and self._validate_password(password1)\
            and query.select_user_name(user_name) is None\
            and query.select_email(email_address) is None\
                and password1 == password2:

            self.logger('Log: Valid User Credentials')
            return True

        else:
            self.logger('Log: Invalid User Credentials')
            return False

    def validate_user_info(self, user_info):
        zip_code = user_info.get('zip')
        phone_number = user_info.get('phone_number')

        try:
            if int(zip_code) and int(phone_number):
                self.logger('Log: Valid Zip and Phone Number')
                return True
            else:
                self.logger('Log: Invalid Values for Zip or Phone Number')
                return False

        except ValueError as Error:
            self.logger(f'Log E {Error}')
            return False

    def validate_manager_id(self, manager_id):
        manager = query.select_manager(manager_id)

        if manager is None:
            self.logger('Log: Invalid ManagerID')
            return
        else:
            self.logger('Log: Valid ManagerID')
            return manager

    def validate_manager_token(self, token):
        session_token = session.get_session('token')

        if token == session_token:
            self.logger('Log: Valid Manager Token')
            return True
        else:
            self.logger('Log: Invalid Manager Token')
            return False

    def validate_bill_config(self, config):
        if config.get('bill_1') == '':
            self.logger('Log: Invalid Bill Configuration - Bill 1 missing')
            return False
        else:
            self.logger('Log: Valid Bill Configuration')
            return True

# ---------------------Bills-------------------------

    # validates that everything going into bills is valid data
    # not currently verifying that the due date is greater than the current date
    # because the users can than see if the manager is being scummy
    def validate_bills(self, bills):
        due_date = bills.pop('due_date')
        raw_due_date = due_date.replace('-', '')

        # checks for valid bill values
        if raw_due_date.isnumeric()and re.search(r'.+-.+-', due_date) and self._valid_date(due_date):
            for key, value in bills.items():
                try:
                    float(value)

                except ValueError as Error:
                    self.logger(f'Log E {Error} - Not an excepted bill value')
                    return False

            bills['due_date'] = due_date
            self.logger(f'Log: All Bill values are valid.')
            return True

        else:
            self.logger('Log: Invalid Due Date value')
            return False

# ----------------------Static Methods-----------------

    @staticmethod
    def _validate_password(password):
        if re.search(r'[a-z]', password)\
                and re.search(r'[0-9]', password)\
                and re.search(r'[A-Z]', password)\
                and len(password) >= 8:

            NewDataValidator.logger('Log: Valid Password')
            return True

        else:
            NewDataValidator.logger('Log: Invalid Password')
            return False

    @staticmethod
    def _validate_email(email):
        if re.search(r'.+@.+\.com', email):
            NewDataValidator.logger('Log: Valid Email')
            return True

        else:
            NewDataValidator.logger('Log: Invalid Email')
            return False

    # Checks if the date can exist, i.e: month 13 does not exist
    @staticmethod
    def _valid_date(date_value):
        try:
            datetime.strptime(date_value, '%Y-%m-%d')
            return True

        except ValueError:
            return False

    @staticmethod
    def logger(message):
        print(message)
