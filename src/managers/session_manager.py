from flask import session


class SessionManager(object):
    def __init__(self):
        pass

    # TODO: Combine setting session methods???
    # sets a user session
    def set_user_session(self, email_address):
        session['email'] = email_address

    # sets a manager token
    def set_token_session(self, token):
        session['token'] = token

    # returns True or False if depending on the session contents
    def check_session(self, key):
        if key in session:
            return True

        return False

    # if the session is valid, returns the email
    def get_session(self, key):
        if self.check_session(key) is False:
            print("Log: No session for " + key)
            return

        print("Log: Active session for " + key)
        return str(session[key])

    def clear_session(self):
        session.clear()
