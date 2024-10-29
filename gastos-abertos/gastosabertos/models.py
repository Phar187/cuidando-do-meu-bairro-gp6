# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry

from cuidando_utils import db


class Execucao(db.Model):

    __tablename__ = 'execucao'

    # id = Column(db.Integer, primary_key=True)
    code = Column(db.String(100), primary_key=True)
    # Official data
    data = Column(postgresql.JSONB)
    # Geodata about this expense line
    point = Column(Geometry('POINT'), default=None)
    # If an attempt were made to gecode this row
    searched = Column(db.Boolean, default=False)

    modifications = relationship('History', backref='execucao')

    state = Column(db.Enum('orcado', 'atualizado', 'empenhado', 'liquidado',
                           name='expense_state'),
                   default='orcado')

    # If it is a 'capital' (4) or 'corrente' (3) expense
    cap_cor = Column(db.Enum('capital', 'corrente', name='capcor'))

    @classmethod
    def get_year(cls):
        return cls.data['cd_anoexecucao']

    @classmethod
    def point_found(cls):
        return cls.point != None  # noqa

    @staticmethod
    def get_region(point):
        """Returns the region of a point."""
        return Regions.query.filter(Regions.geo.ST_Contains(point))

    def get_notification_id(self):
        '''Used to identify this object to the notification system.'''
        return 'cuidandodomeubairro/despesa/' + self.code


class Regions(db.Model):

    __tablename__ = 'regions'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    geo = Column(Geometry('POLYGON'))

    @staticmethod
    def get_points(region):
        """Returns the points inside a region."""
        return Execucao.query.filter(Execucao.point.ST_Within(region))


class History(db.Model):

    __tablename__ = 'execucao_history'

    id = Column(db.Integer, primary_key=True)
    code = Column(db.String(100), ForeignKey('execucao.code'))
    event = Column(db.String(20))
    date = Column(db.DateTime, nullable=False)
    data = Column(postgresql.JSONB)
    notification_sent = Column(db.Boolean, default=False, nullable=False)


class ExecucaoYearInfo(db.Model):

    __tablename__ = 'execucao_year_info'

    year = Column(db.Integer, primary_key=True)
    data = Column(postgresql.JSONB)
