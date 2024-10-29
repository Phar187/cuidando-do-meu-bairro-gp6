"""empty message

Revision ID: de25fa2a8575
Revises: 3b7f58ea72e7
Create Date: 2018-05-30 23:26:11.628030

"""

# revision identifiers, used by Alembic.
revision = 'de25fa2a8575'
down_revision = '3b7f58ea72e7'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserMessage(Base):
    '''Messages sent by users to start a Pedido or a Recurso.'''
    __tablename__ = 'pre_pedido'
    id = sa.Column(sa.Integer, primary_key=True)
    state = sa.Column(sa.String(255))


def upgrade():
    bind = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=bind)

    msgs = session.query(UserMessage).all()
    for msg in msgs:
        msg.state = msg.state.lower()
    session.commit()


def downgrade():
    pass
