class BillAccount(object):
    def __init__(self, account_name, account_type, manager_id, account_id):
        self.account_id = account_id
        self.account_name = account_name
        self.account_type = account_type
        self.manager_id = manager_id
