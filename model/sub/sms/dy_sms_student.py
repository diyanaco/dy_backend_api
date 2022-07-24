from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from model.sub.sms.dy_sms_student_class_link import  association_student_class_table
from backend import Base

class StudentModel(Base):
    __tablename__="dy_sms_student"
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("dy_shared_user.id"))
    class_id = relationship("Child", secondary=association_student_class_table)
    parent = relationship("Parent", back_populates="children")
    fav_sub = Column(String(50))