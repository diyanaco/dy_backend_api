from sqlalchemy import Column, Integer, String, ForeignKey
from backend import Base

class LevelModel(Base):
    __tablename__ = 'dy_sms_level'
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    employee_id = Column(String(50), ForeignKey("dy_sms_employee.id"))
    
    def __repr__(self):
       return "<Subject(name='%s')>" % (self.name)