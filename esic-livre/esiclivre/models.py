# coding: utf-8

import enum

import arrow
import sqlalchemy as sa
from flask import current_app
import sqlalchemy_utils as sa_utils
from sqlalchemy.orm.exc import NoResultFound

from cuidando_utils import db


pedido_attachments = sa.Table(
    'pedido_attachments', db.metadata,
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id')),
    db.Column('attachment_id', db.Integer, db.ForeignKey('attachment.id'))
)

pedido_keyword = sa.Table(
    'pedido_keyword', db.metadata,
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'))
)

pedido_author = sa.Table(
    'pedido_author', db.metadata,
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


class PedidosUpdate(db.Model):
    __tablename__ = 'pedidos_update'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(sa_utils.ArrowType, index=True)


class UserMessage(db.Model):
    '''Messages sent by users to start a Pedido or a Recurso.'''
    __tablename__ = 'pre_pedido'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    orgao_name = db.Column(db.String(255), nullable=False, default='')
    text = db.Column(sa.UnicodeText(), nullable=False)
    created_at = db.Column(sa_utils.ArrowType, nullable=False)
    updated_at = db.Column(sa_utils.ArrowType)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=True)

    # separated by commas
    keywords = db.Column(db.String(255), nullable=False, default='')

    states = enum.Enum('UserMessageStates', 'waiting processed')
    state = db.Column(db.Enum(states), default=states.waiting, nullable=False)

    types = enum.Enum('UserMessageTypes', 'pergunta recurso')
    type = db.Column(db.Enum(types), nullable=False)

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'orgao_name': self.orgao_name,
            'text': self.text,
            'keywords': [keyword for keyword in self.keywords.split(',')],
            'state': self.state,
            'type': self.type
        }

    @property
    def orgao(self):
        return Orgao.query.filter_by(name=self.orgao_name).one()

    @property
    def author(self):
        return Author.query.filter_by(id=self.author_id).one()

    @property
    def all_keywords(self):
        return [
            Keyword.query.filter_by(name=k).one()
            for k in self.keywords.split(',')  # noqa
        ]

    def create_pedido(self, protocolo, deadline):
        pedido = Pedido(
            protocol=protocolo,
            deadline=deadline,
            orgao_name=self.orgao_name,
            author=self.author,
            keywords=self.all_keywords,
            description=self.text,
            request_date=arrow.utcnow())
        db.session.add(pedido)
        db.session.commit()
        self.updated_at = arrow.utcnow()
        self.state = UserMessage.states.processed
        # db.session.add(self)
        db.session.commit()
        return pedido


class Pedido(db.Model):
    __tablename__ = 'pedido'

    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.Integer, index=True, unique=True, nullable=True)
    interessado = db.Column(db.String(255))
    situation = db.Column(db.String(255), index=True)
    request_date = db.Column(sa_utils.ArrowType, index=True)
    contact_option = db.Column(db.String(255), nullable=True)
    description = db.Column(sa.UnicodeText())
    deadline = db.Column(sa_utils.ArrowType, index=True, nullable=True)
    orgao_name = db.Column(db.String(255), nullable=True)
    # If this Pedido is open to Recursos at the moment.
    allow_recurso = db.Column(db.Boolean, default=False, nullable=False)
    history = db.relationship('Message', backref='pedido', order_by='Message.date')
    keywords = db.relationship('Keyword', secondary=pedido_keyword, backref='pedidos')
    user_messages = db.relationship('UserMessage', backref='pedido')
    author = db.relationship(
        'Author', secondary=pedido_author, backref='pedidos', uselist=False
    )
    attachments = db.relationship(
        'Attachment', secondary=pedido_attachments, backref='pedido'
    )

    def get_notification_id(self):
        '''Used to identify this object to the notification system.'''
        # return 'cuidandodomeubairro/pedido/protocolo/' + str(self.protocol)
        return 'cuidandodomeubairro/pedido/id/' + str(self.id)

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'protocol': self.protocol,
            'notification_id': self.get_notification_id(),
            'notification_author': current_app.config['VIRALATA_USER'],
            'interessado': self.interessado,
            'situation': self.situation,
            'allow_recurso': self.allow_recurso,
            'request_date': self.request_date.isoformat() if self.request_date else '',
            'contact_option': self.contact_option,
            'description': self.description,
            'deadline': self.deadline.isoformat() if self.deadline else '',
            'orgao_name': self.orgao_name,
            'history': [m.as_dict for m in self.history],
            'author': self.author.as_dict,
            'keywords': [kw.as_dict for kw in self.keywords],
            'attachments': [att.as_dict for att in self.attachments]
        }

    def add_keyword(self, keyword_name):
        try:
            keyword = (db.session.query(Keyword)
                       .filter_by(name=keyword_name).one())
        except NoResultFound:
            keyword = Keyword(name=keyword_name)
            db.session.add(keyword)
            db.session.commit()
        self.keywords.append(keyword)


class OrgaosUpdate(db.Model):
    __tablename__ = 'orgaos_update'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(sa_utils.ArrowType, index=True)


class Orgao(db.Model):
    __tablename__ = 'orgao'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    @property
    def as_dict(self):
        return self.name


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    situation = db.Column(db.String(255))
    justification = db.Column(sa.UnicodeText())
    responsible = db.Column(db.String(255))
    date = db.Column(sa_utils.ArrowType, index=True)
    pedido_id = db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id'))
    notification_sent = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'situation': self.situation,
            'justification': self.justification,
            'responsible': self.responsible,
            'date': self.date.isoformat(),
            'pedido_id': self.pedido_id,
        }


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    @property
    def as_dict(self):
        return self.name


class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)

    @property
    def as_dict(self):
        return self.name


class Attachment(db.Model):
    __tablename__ = 'attachment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(sa_utils.ArrowType)
    ia_url = db.Column(sa_utils.URLType)

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ia_url': self.ia_url
        }
