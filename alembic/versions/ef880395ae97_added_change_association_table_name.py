"""Added change association table name

Revision ID: ef880395ae97
Revises: 64985f9ca324
Create Date: 2022-07-24 14:47:20.653079

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef880395ae97'
down_revision = '64985f9ca324'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dy_sms_student_class_link', sa.Column('student_id', sa.String(length=50), nullable=True))
    op.add_column('dy_sms_student_class_link', sa.Column('class_id', sa.String(length=50), nullable=True))
    op.drop_constraint('dy_sms_student_class_link_ibfk_2', 'dy_sms_student_class_link', type_='foreignkey')
    op.drop_constraint('dy_sms_student_class_link_ibfk_1', 'dy_sms_student_class_link', type_='foreignkey')
    op.create_foreign_key(None, 'dy_sms_student_class_link', 'dy_sms_student', ['student_id'], ['id'])
    op.create_foreign_key(None, 'dy_sms_student_class_link', 'dy_sms_class', ['class_id'], ['id'])
    op.drop_column('dy_sms_student_class_link', 'left_id')
    op.drop_column('dy_sms_student_class_link', 'right_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dy_sms_student_class_link', sa.Column('right_id', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('dy_sms_student_class_link', sa.Column('left_id', mysql.VARCHAR(length=50), nullable=True))
    op.drop_constraint(None, 'dy_sms_student_class_link', type_='foreignkey')
    op.drop_constraint(None, 'dy_sms_student_class_link', type_='foreignkey')
    op.create_foreign_key('dy_sms_student_class_link_ibfk_1', 'dy_sms_student_class_link', 'dy_sms_student', ['left_id'], ['id'])
    op.create_foreign_key('dy_sms_student_class_link_ibfk_2', 'dy_sms_student_class_link', 'dy_sms_class', ['right_id'], ['id'])
    op.drop_column('dy_sms_student_class_link', 'class_id')
    op.drop_column('dy_sms_student_class_link', 'student_id')
    # ### end Alembic commands ###
