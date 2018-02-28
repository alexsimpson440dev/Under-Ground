class Manager(object):
    def __init__(self, user_id, manager_id=None):
        self.manager_id = manager_id
        self.user_id = user_id