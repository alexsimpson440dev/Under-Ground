from src.queries.insert import Insert
from src.queries.select import Select

insert = Insert()
select = Select()


class QueryManager(object):
    def __init__(self):
        pass

# --------------------SELECT QUERIES--------------------------------------------
    # select user_name
    def select_user_name(self, user_name):
        args = select.select_user_name(user_name)
        return args

    # select email_address
    def select_email_address(self, email_address):
        args = select.select_email(email_address)
        return args

    # select bill account
    def select_bill_account(self, manager_id):
        args = select.select_bill_account(manager_id)
        return args

    def select_manager(self, manager_id):
        args = select.select_manager_object(manager_id)
        return args

# --------------------INSERT QUERIES--------------------------------------------
    # inserts user
    def insert_user(self, user):
        insert.insert_object(user)

    def insert_user_info(self, user_info):
        insert.insert_object(user_info)

# --------------------UPDATE QUERIES--------------------------------------------

# --------------------DELETE QUERIES--------------------------------------------
