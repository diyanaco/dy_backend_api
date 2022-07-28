from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from backend import Base

association_student_package_set_table = Table(
    "dy_sms_student_package_set_link",
    Base.metadata,
    Column("package_set_id", ForeignKey("dy_sms_package_set.id")),
    Column("student_id", ForeignKey("dy_sms_student.id")),
)