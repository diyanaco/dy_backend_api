from sqlalchemy import Column, Integer, String, ForeignKey,  DateTime
from backend import Base

class LevelModel(Base):
    __tablename__ = 'dy_sms_level'
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    rank = Column(Integer)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    
    def __repr__(self):
       return "<Subject(name='%s')>" % (self.name)