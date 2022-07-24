from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from backend import Base

association_student_class_table = Table(
    "dy_sms_student_class_link",
    Base.metadata,
    Column("student_id", ForeignKey("dy_sms_student.id")),
    Column("class_id", ForeignKey("dy_sms_class.id")),
)