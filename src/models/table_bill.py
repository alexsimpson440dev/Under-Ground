class Bill(object):
    def __init__(self, bill_config_id, date, bill_c_1, bill_c_2, bill_c_3, bill_c_4, bill_c_5,
                 total_pp, total, due_date, bill_id=None):
        self.bill_id = bill_id
        self.bill_config_id = bill_config_id
        self.date = date
        self.bill_c_1 = bill_c_1
        self.bill_c_2 = bill_c_2
        self.bill_c_3 = bill_c_3
        self.bill_c_4 = bill_c_4
        self.bill_c_5 = bill_c_5
        self.total_pp = total_pp
        self.total = total
        self.due_date = due_date