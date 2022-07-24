from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend import Base

#TODO: #28 Implement One to One relationship between
#User and Student table, one user can only be one student, and one student can only be one user
class UserModel(Base):
    __tablename__ = 'dy_shared_user'
    id = Column(String(50), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(200))
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    student = relationship("StudentModel", uselist=False, backref="dy_shared_user")
    
    def __repr__(self):
       return "<User(first_name='%s', last_name='%s')>" % (self.first_name, self.last_name)

