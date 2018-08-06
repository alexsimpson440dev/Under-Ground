from src.database import Database
from datetime import date

from src.models.table_user import User
from src.models.table_user_info import UserInfo
from src.models.table_manager import Manager
from src.models.table_bill import Bill
from src.models.table_bill_config import BillConfig
from src.models.table_bill_account import BillAccount
from src.models.table_paid import Paid

db = Database()

user1 = User('alex', 'email', 'pa')
manager1 = Manager(user1)
bill_account1 = BillAccount('account', 'personal', manager1)
info1 = UserInfo('a', 's', '3', 'a', 'mn', 'zip', 'phone', user1, bill_account1)
bill_config1 = BillConfig('1', '2', '3', '4', '5', bill_account1)
bill = Bill(date(1000, 1, 1), 1, 2, 3, 4, 5, 1, 1, date(1000, 1, 1), bill_config1)
paid = Paid(1, False, bill)

db.session.add(user1)
db.session.add(manager1)
db.session.add(bill_account1)
db.session.add(info1)
db.session.add(bill_config1)
db.session.add(bill)
db.session.add(paid)

db.session.commit()
db.session.close()
