"""Added fields for student table

Revision ID: 8a394ebe742f
Revises: c04bca259ef5
Create Date: 2022-07-27 22:41:25.704573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8a394ebe742f'
down_revision = 'c04bca259ef5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dy_sms_student', sa.Column('guardian_id', sa.String(length=50), nullable=True))
    op.add_column('dy_sms_student', sa.Column('package_set_id', sa.String(length=50), nullable=True))
    op.add_column('dy_sms_student', sa.Column('education_id', sa.String(length=50), nullable=True))
    op.add_column('dy_sms_student', sa.Column('level_id', sa.String(length=50), nullable=True))
    op.create_foreign_key(None, 'dy_sms_student', 'dy_shared_education', ['education_id'], ['id'])
    op.create_foreign_key(None, 'dy_sms_student', 'dy_sms_guardian', ['guardian_id'], ['id'])
    op.create_foreign_key(None, 'dy_sms_student', 'dy_sms_level', ['level_id'], ['id'])
    op.create_foreign_key(None, 'dy_sms_student', 'dy_sms_package', ['package_set_id'], ['id'])
    op.drop_column('dy_sms_subject', 'teacher')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dy_sms_subject', sa.Column('teacher', mysql.VARCHAR(length=50), nullable=True))
    op.drop_constraint(None, 'dy_sms_student', type_='foreignkey')
    op.drop_constraint(None, 'dy_sms_student', type_='foreignkey')
    op.drop_constraint(None, 'dy_sms_student', type_='foreignkey')
    op.drop_constraint(None, 'dy_sms_student', type_='foreignkey')
    op.drop_column('dy_sms_student', 'level_id')
    op.drop_column('dy_sms_student', 'education_id')
    op.drop_column('dy_sms_student', 'package_set_id')
    op.drop_column('dy_sms_student', 'guardian_id')
    # ### end Alembic commands ###
