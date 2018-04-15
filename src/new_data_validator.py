from src.query_manager import QueryManager
import re

query = QueryManager()

class NewDataValidator(object):
    def __init__(self):
        pass

    def validate_user(self, user):
        user_name = user.get('user_name')
        email_address = user.get('email_address')
        password1 = user.get('password1')
        password2 = user.get('password2')

        if user_name != "":
            if self._validate_email(email_address) is True:
                if self._validate_password(password1) is True:
                    if query.select_user_name(user_name) is None:
                        if query.select_email_address(email_address) is None:
                            if password1 == password2:
                                query.insert_user(user_name, email_address, password1)
                                return True

        else:
            return False

    @staticmethod
    def _validate_password(password):
        if re.search(r'[a-z]', password):
            if re.search(r'[1-9]', password):
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
