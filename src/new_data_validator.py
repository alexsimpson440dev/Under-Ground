from src.query_manager import QueryManager

query = QueryManager()

class NewDataValidator(object):
    def __init__(self):
        pass

    def validate_user(self, user):
        user_name = user.get('user_name')
        email_address = user.get('email_address')
        password1 = user.get('password1')
        password2 = user.get('password2')

        return query.select_email_address(email_address)
