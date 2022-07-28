from backend import Base 
from sqlalchemy import Column, ForeignKey, String, Float, DateTime

class PaymentModel(Base):
    __tablename__ = "dy_sms_payment"
    id = Column(String(50))
    name = Column(String(50))
    student_id = Column(String(50), ForeignKey("dy_sms_student.id"))
    amount = Column(Float())    
    created_date = Column(DateTime)
    update_date = Column(DateTime)

    def __repr__(self):
       return "<Payment(name='%s')>" % (self.name)