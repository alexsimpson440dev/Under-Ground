from flask import session


class SessionManager(object):
    def __init__(self):
        pass

    def set_user_session(self, email_address):
        session['email'] = email_address

    def set_token_session(self, token):
        session['token'] = token

    def check_session(self, key):
        if key in session:
            return True

        return False

    def get_session(self, key):
        if self.check_session(key) is False:
            return

        return str(session[key])
