from flask import session


class SessionManager(object):
    def __init__(self):
        pass

    # sets a session
    def set_session(self, key, value):
        self.logger('Log: New Session ' + key + ' - ' + str(value))
        session[key] = value

    # returns True or False if depending on the session contents
    def check_session(self, key):
        self.logger('Log: Checking ' + key + ' Session')
        if key in session:
            self.logger('Log: Active Session ' + key + ' - ' + str(session[key]))
            return True

        self.logger("Log: No Active Session for " + key)
        return False

    # if the session is valid, returns the email
    def get_session(self, key):
        if self.check_session(key) is False:
            return

        return str(session[key])

    def clear_session(self, key):
        self.logger('Log: Removing Active Session for ' + key)
        session.pop(key, None)

    @staticmethod
    def logger(message):
        print(message)
