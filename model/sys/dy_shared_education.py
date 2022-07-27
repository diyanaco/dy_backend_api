from backend import Base
from sqlalchemy import Column, String
class EducationModel(Base):
    __tablename__="dy_shared_education"
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    type = Column(String(50))

    def __repr__(self):
        return "<Education(name='%s', type='%s')" % (self.name, self.type)
