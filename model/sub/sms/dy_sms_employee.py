from backend import Base
from sqlalchemy import Column, ForeignKey, String

class EmployeeModel(Base):
    __tablename__ = "dy_sms_employee"
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    user_id = Column(String(50), ForeignKey("dy_shared_user.id"))

    def __repr__(self):
       return "<Employee(name='%s', user_id='%s')>" % (self.name, self.user_id)