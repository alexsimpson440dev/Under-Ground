from sqlalchemy import Column, Integer, Date, Float, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Bill(Base):

    __tablename__ = 'bill'

    bill_id = Column(Integer, Sequence('article_aid_seq', start=50001, increment=1, optional=True), primary_key=True)
    bill_config_id = Column(Integer, ForeignKey('bill_config.bill_config_id'))
    date = Column('date', Date)
    bill_c_1 = Column(Float)
    bill_c_2 = Column(Float)
    bill_c_3 = Column(Float)
    bill_c_4 = Column(Float)
    bill_c_5 = Column(Float)
    total_pp = Column(Float)
    total = Column(Float)
    due_date = Column(Date)

    bill_configs = relationship("BillConfig", backref="bill")

    def __init__(self, date, bill_c_1, bill_c_2, bill_c_3, bill_c_4, bill_c_5, total_pp, total, due_date, bill_configs, bill_id=None):
        self.bill_id = bill_id
        self.date = date
        self.bill_c_1 = bill_c_1
        self.bill_c_2 = bill_c_2
        self.bill_c_3 = bill_c_3
        self.bill_c_4 = bill_c_4
        self.bill_c_5 = bill_c_5
        self.total_pp = total_pp
        self.total = total
        self.due_date = due_date
        # relationships
        self.bill_configs = bill_configs
