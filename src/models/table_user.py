class User(object):
    def __init__(self, username, email_address, password, user_id=None, user_type=3):
        self.user_id = user_id
        self.user_type = user_type
        self.user_name = username
        self.email_address = email_address
        self.password = password
