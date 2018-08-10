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

# Returns a filtered object
# --------------------SELECT QUERIES--------------------------------------------
    def select_email(self, email_address):
        for user in db.session.query(User).filter(User.email_address == email_address):
            db.session.close()
            return user

    def select_user_name(self, user_name):
        for user in db.session.query(User).filter(User.user_name == user_name):
            db.session.close()
            return user

    def select_user_info(self, user_id):
        for user_info in db.session.query(UserInfo).filter(UserInfo.user_id == user_id):
            db.session.close()
            return user_info

    def select_bill_account(self, manager_id):
        for account in db.session.query(BillAccount).filter(BillAccount.manager_id == manager_id):
            db.session.close()
            return account

    def select_manager(self, manager_id):
        for manager in db.session.query(Manager).filter(Manager.manager_id == manager_id):
            db.session.close()
            return manager

    def select_manager_uid(self, user_id):
        for manager in db.session.query(Manager).filter(Manager.user_id == user_id):
            db.session.close()
            return manager

    def select_bill_config(self, account_id):
        for config in db.session.query(BillConfig).filter(BillConfig.account_id == account_id):
            db.session.close()
            return config

# --------------------INSERT QUERIES--------------------------------------------
    # inserts an object
    def insert(self, object):
        db.session.add(object)
        return

# --------------------UPDATE QUERIES--------------------------------------------

# --------------------DELETE QUERIES--------------------------------------------
