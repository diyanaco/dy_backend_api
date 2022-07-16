from sqlalchemy import Column, Integer, String
from backend import Base

class UserModel(Base):
    __tablename__ = 'dy_shared_user'
    id = Column(String(50), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    
    def __repr__(self):
       return "<User(first_name='%s', last_name='%s')>" % (self.first_name, self.last_name)

