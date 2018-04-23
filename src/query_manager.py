from src.queries.insert import Insert
from src.queries.select import Select
from src.models.table_user import User
from src.models.table_user_info import UserInfo

import bcrypt

insert = Insert()
select = Select()

class QueryManager(object):
    def __init__(self):
        pass

#--------------------SELECT QUERIES--------------------------------------------
    # select user_name
    def select_user_name(self, user_name):
        args = select.select_user_name(user_name)
        return args

    # select email_address
    def select_email_address(self, email_address):
        args = select.select_email(email_address)
        return args

#--------------------INSERT QUERIES--------------------------------------------
    # inserts user
    def insert_user(self, user):
        insert.insert_object(user)

    def insert_user_info(self, user_info):
        bill_account = "get" # get using the manager_id

        insert.insert_object(user_info)

#--------------------UPDATE QUERIES--------------------------------------------

#--------------------DELETE QUERIES--------------------------------------------
