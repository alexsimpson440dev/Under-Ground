from flask import session

class SessionAPI(object):
    def __init__(self):
        pass

    def get_session(self, email_address):
        session['email'] = email_address

    def check_session(self):
        if 'email' in session:
            return True
        else:
            return False

