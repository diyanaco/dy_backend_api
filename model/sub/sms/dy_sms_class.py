from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from model.sub.sms.dy_sms_student_class_link import association_student_class_table
from backend import Base

class ClassModel(Base):
    __tablename__ = "dy_sms_class"
    id = Column(String(50), primary_key = True)
    name = Column(String(10))
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    #Many to many relationship
    student_id = relationship("StudentModel", secondary=association_student_class_table)

    def __repr__(self):
        return "<Class(name='%s', student_id'%s')>" % (self.name, self.student_id)