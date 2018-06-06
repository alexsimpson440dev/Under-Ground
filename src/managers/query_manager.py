from src.models import User, UserInfo, Manager, BillAccount, Bill, BillConfig
from src.database import Database

db = Database()


class QueryManager(object):
    def __init__(self):
        pass

    def session_commit(self):
        db.session.commit()

    def session_close(self):
        db.session.close()

# --------------------SELECT QUERIES--------------------------------------------
    def select_email(self, email_address):
        for user in db.session.query(User.email_address).filter(User.email_address == email_address):
            return user.email_address

    def select_user_name(self, user_name):
        for user in db.session.query(User.user_name).filter(User.user_name == user_name):
            return user.user_name

    def select_user(self, email_address):
        for user in db.session.query(User).filter(User.email_address == email_address):
            return user

    def select_bill_account(self, manager_id):
        for account in db.session.query(BillAccount).filter(BillAccount.manager_id == manager_id):
            return account

    def select_manager(self, manager_id):
        for manager in db.session.query(Manager).filter(Manager.manager_id == manager_id):
            return manager

    def select_manager_uid(self, user_id):
        for manager in db.session.query(Manager).filter(Manager.user_id == user_id):
            return manager

# --------------------INSERT QUERIES--------------------------------------------
    # inserts an object
    def insert(self, object):
        db.session.add(object)
        return

# --------------------UPDATE QUERIES--------------------------------------------

# --------------------DELETE QUERIES--------------------------------------------
