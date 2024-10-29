"""Add OrgaosUpdate Table.

Revision ID: 21bf24bc247d
Revises: None
Create Date: 2015-11-28 15:37:10.583148

"""

# revision identifiers, used by Alembic.
revision = '21bf24bc247d'
down_revision = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    op.create_table(
        'orgaos_update',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date',
                  sqlalchemy_utils.types.arrow.ArrowType(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_orgaos_update_date'),
                    'orgaos_update', ['date'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_orgaos_update_date'), table_name='orgaos_update')
    op.drop_table('orgaos_update')
