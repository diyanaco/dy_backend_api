from backend import Base
from sqlalchemy import Column, String, DateTime

class GuardianModel(Base):
    __tablename__ = "dy_sms_guardian"
    id = Column(String(50), primary_key=True)
    primary_name = Column(String(50))
    secondary_name = Column(String(50))
    created_date = Column(DateTime)
    update_date = Column(DateTime)

    def __repr__(self) -> str:
        return "<Guardian(primary_name='%s', secondary_name='%s')" % (
            self.primary_name,
            self.secondary_name
        )