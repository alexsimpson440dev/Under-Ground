from src.models import User, UserInfo, Manager, BillAccount, Bill, BillConfig, Paid
from src.database import Database
from sqlalchemy import select, and_, update, distinct

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
            return user

    def select_user_name(self, user_name):
        for user in db.session.query(User).filter(User.user_name == user_name):
            return user

    def select_user_info(self, user_id):
        for user_info in db.session.query(UserInfo).filter(UserInfo.user_id == user_id):
            return user_info

    def select_user_count_by_account_id(self, account_id):
        user_info = db.session.query(UserInfo).filter(UserInfo.account_id == account_id)
        return user_info

    def select_bill_account(self, manager_id):
        for account in db.session.query(BillAccount).filter(BillAccount.manager_id == manager_id):
            return account

    def select_manager(self, manager_id):
        for manager in db.session.query(Manager).filter(Manager.manager_id == manager_id):
            return manager

    def select_manager_uid(self, user_id):
        for manager in db.session.query(Manager).filter(Manager.user_id == user_id):
            return manager

    def select_bill_config(self, account_id):
        for config in db.session.query(BillConfig).filter(BillConfig.account_id == account_id):
            return config

    def select_bill_by_config_id(self, bill_config_id):
        bill = db.session.query(Bill.date, Bill.bill_c_1, Bill.bill_c_2, Bill.bill_c_3, Bill.bill_c_4,
                                Bill.bill_c_5, Bill.total, Bill.due_date).\
            filter(Bill.bill_config_id == bill_config_id)

        return bill

    def select_bill_pay(self, bill_config_id, user_id):
        bill = db.session.query(Bill.bill_id, Bill.date, Bill.bill_c_1, Bill.bill_c_2, Bill.bill_c_3, Bill.bill_c_4,
                                Bill.bill_c_5, Bill.total, Bill.due_date, Paid.paid).distinct().\
            filter(Bill.bill_config_id == bill_config_id, Paid.user_id == user_id, Bill.bill_id == Paid.bill_id)

        return bill

    def select_paid_by_user(self, user_id):
        paid = db.session.query(Paid.bill_id, Paid.paid).filter(Paid.user_id == user_id)
        paid = dict(paid)

        return paid

    def select_index_page_info_manager(self, account_id):
        results = db.session.query(UserInfo.first_name, UserInfo.last_name, User.email_address).distinct().\
            filter(UserInfo.account_id == account_id, User.user_id == UserInfo.user_id)

        return results

# --------------------INSERT QUERIES--------------------------------------------
    # inserts an object
    def insert(self, object):
        db.session.add(object)
        db.session.commit()
        return


# --------------------UPDATE QUERIES--------------------------------------------
    # updates pay to true
    def update_paid(self, bill_id):
        db.session.query(Paid).filter(Paid.bill_id == bill_id).update({"paid": True})
        db.session.commit()
        return

# --------------------DELETE QUERIES--------------------------------------------
