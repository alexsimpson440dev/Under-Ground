class UserInfo(object):
    def __init__(self, user_id, manager_id, account_id, first_name, last_name, address, city, state, zip, phone, info_id=None):
        self.info_id = info_id
        self.user_id = user_id
        self.manager_id = manager_id
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone = phone
