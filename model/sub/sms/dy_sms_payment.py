from backend import Base 
from sqlalchemy import Column, ForeignKey, String, Float

class PaymentModel(Base):
    __tablename__ = "dy_sms_payment"
    id = Column(String(50))
    name = Column(String(50))
    student_id = Column(String(50), ForeignKey("dy_sms_student.id"))
    amount = Column(Float())