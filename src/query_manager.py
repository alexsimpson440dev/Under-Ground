from src.queries.insert import Insert
from src.queries.select import Select

from src.database import Database()

insert = Insert()
select = Select()

db = Database()


class QueryManager(object):
    def __init__(self):
        pass

    def commit(self):
        db.session.commit()

    def close(self):
        db.session.close()

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

    def select_user_id(self, email_address):
        args = select.select_user_id(email_address)
        return args

# --------------------INSERT QUERIES--------------------------------------------
    # inserts user
    def insert(self, object):
        db.session.add(object)
        return

# --------------------UPDATE QUERIES--------------------------------------------

# --------------------DELETE QUERIES--------------------------------------------
