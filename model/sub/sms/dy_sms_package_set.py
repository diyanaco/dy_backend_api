from backend import Base 
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from model.sub.sms.dy_sms_student_package_set_link import association_student_package_set_table

class PackageSetModel(Base):
    __tablename__ = "dy_sms_package_set"
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    created_date = Column(DateTime)
    update_date = Column(DateTime)
    #Many to many relationship
    student_id = relationship("StudentModel", secondary=association_student_package_set_table)