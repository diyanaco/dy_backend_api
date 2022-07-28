from colorama import Fore
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship
from model.sub.sms.dy_sms_student_class_link import  association_student_class_table
from model.sub.sms.dy_sms_student_package_set_link import association_student_package_set_table
from backend import Base
#TODO #41 Update student model according to dbSchema
class StudentModel(Base):
    __tablename__="dy_sms_student"
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("dy_shared_user.id"))
    fav_sub = Column(String(50))
    guardian_id = Column(String(50), ForeignKey("dy_sms_guardian.id"))
    education_id = Column(String(50), ForeignKey("dy_shared_education.id"))
    level_id = Column(String(50), ForeignKey("dy_sms_level.id"))
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    #TODO #48 Implement created and updated by user_id

    #Many to Many 
    class_id = relationship("ClassModel", secondary=association_student_class_table)
    #Many to Many 
    package_set_id = relationship("PackageSetModel", secondary=association_student_package_set_table)
    #Many to One
    user = relationship("UserModel", backref="dy_sms_student")

    def __repr__(self):
       return "<Subject(name='%s',user_id='%s', fav_sub='%s'.)>" % (self.name, self.user_id, self.fav_sub)