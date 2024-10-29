"""empty message

Revision ID: ebb84b9e2f6e
Revises: 21bf24bc247d
Create Date: 2018-05-18 19:05:55.187662

"""

# revision identifiers, used by Alembic.
revision = 'ebb84b9e2f6e'
down_revision = '21bf24bc247d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Remove multiple revision values
    op.get_bind().execute(sa.sql.text('''
    DELETE FROM alembic_version WHERE version_num='21bf24bc247d';
    INSERT INTO alembic_version VALUES ('21bf24bc247d');
    '''))
    op.alter_column('message', 'pedido_id', existing_type=sa.INTEGER(), nullable=True)


def downgrade():
    op.alter_column('message', 'pedido_id', existing_type=sa.INTEGER(), nullable=False)
