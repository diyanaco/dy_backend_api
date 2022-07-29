from backend import Base
from sqlalchemy import Column, ForeignKey, String, DateTime

class BranchModel(Base):
    __tablename__="dy_shared_branch"
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    education_id = Column(String(50), ForeignKey("dy_shared_education.id"))
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    def __repr__(self):
        return "<Branch(name='%s', type='%s')>" % (self.name, self.type)
