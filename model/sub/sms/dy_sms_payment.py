from backend import Base 
from sqlalchemy import Column, ForeignKey, String, Float, DateTime

class PaymentModel(Base):
    __tablename__ = "dy_sms_payment"
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    student_id = Column(String(50), ForeignKey("dy_sms_student.id"))
    amount = Column(Float(10))    
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    def __repr__(self):
       return "<Payment(name='%s', amount='%s')>" % (self.name, self.amount)