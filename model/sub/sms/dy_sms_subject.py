from sqlalchemy import Column, Integer, String
from backend import Base

class SubjectModel(Base):
    __tablename__ = 'dy_sms_subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
       return "<Subject(name='%s')>" % (self.name)

