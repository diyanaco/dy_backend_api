from sqlalchemy import Column, ForeignKey, Integer, String
from backend import Base

class SubjectModel(Base):
    __tablename__ = 'dy_sms_subject'
    id = Column(String(50), primary_key=True)
    name = Column(String(50))

    def __repr__(self):
       return "<Subject(name='%s')>" % (self.name)

