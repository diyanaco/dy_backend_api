from sqlalchemy import Column, Integer, String
from backend import Base

class PackageModel(Base):
    __tablename__ = 'dy_sms_package'
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    
    def __repr__(self):
       return "<Subject(name='%s')>" % (self.name)