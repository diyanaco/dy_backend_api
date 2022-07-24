from sqlalchemy import Column, Integer, String
from backend import Base

class ClassModel(Base):
    __tablename__ = "dy_sms_class"
    id = Column(String(50), primary_key = True)
    name = Column(String(10))

    def __repr__(self):
        return "<Class(name='%s')>" % (self.name)