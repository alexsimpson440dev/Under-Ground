class BillAccount(object):
    def __init__(self, manager_id, account_name, account_type, account_id=None):
        self.account_id = account_id
        self.manager_id = manager_id
        self.account_name = account_name
        self.account_type = account_type
