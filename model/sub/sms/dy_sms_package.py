from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from backend import Base

class PackageModel(Base):
    __tablename__ = 'dy_sms_package'
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    level_id = Column(String(50), ForeignKey("dy_sms_level.id"))
    package_set_id = Column(String(50), ForeignKey("dy_sms_package_set.id"))
    subject_id = Column(String(50), ForeignKey("dy_sms_subject.id"))
    created_date = Column(DateTime)
    update_date = Column(DateTime)    
    def __repr__(self):
       return "<Subject(name='%s')>" % (self.name)