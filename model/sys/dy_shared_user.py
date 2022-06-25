from sqlalchemy import Column, Integer, String
from backend import Base

class User(Base):
    __tablename__ = 'dy_shared_user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    def __repr__(self):
       return "<User(first_name='%s', last_name='%s')>" % (
                            self.first_name, self.last_name)

