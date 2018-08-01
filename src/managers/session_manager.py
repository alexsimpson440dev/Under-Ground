from flask import session


class SessionManager(object):
    def __init__(self):
        pass

    # sets a session
    def set_session(self, key, value):
        print('Log: New Session ' + key + ' - ' + str(value))
        session[key] = value

    # old session adding todo: remove after testing
    '''def set_user_session(self, email_address):
        print('Log: Set session Email - ' + email_address)
        session['email'] = email_address

    # sets a manager token
    def set_token_session(self, token):
        session['token'] = token'''
    # ---------------------------------------------------------

    # returns True or False if depending on the session contents
    def check_session(self, key):
        print('Log: Checking ' + key + ' Session')
        if key in session:
            print('Log: Active Session ' + key + ' - ' + str(session[key]))
            return True

        print("Log: No Active Session for " + key)
        return False

    # if the session is valid, returns the email
    def get_session(self, key):
        if self.check_session(key) is False:
            return

        return str(session[key])

    def clear_session(self):
        print('Log: Removing Active Sessions')
        session.clear()
