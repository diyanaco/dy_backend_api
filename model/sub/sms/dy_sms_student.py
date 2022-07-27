from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship
from model.sub.sms.dy_sms_student_class_link import  association_student_class_table
from backend import Base
#TODO #41 Update student model according to dbSchema
class StudentModel(Base):
    __tablename__="dy_sms_student"
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("dy_shared_user.id"))
    fav_sub = Column(String(50))
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    #Many to Many 
    class_id = relationship("ClassModel", secondary=association_student_class_table)

    #Many to One
    user = relationship("UserModel", backref="dy_sms_student")