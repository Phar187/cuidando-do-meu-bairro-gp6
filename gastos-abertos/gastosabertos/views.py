# coding: utf-8

from __future__ import unicode_literals  # unicode by default
import json

from flask import current_app
from flask_restplus import Resource
from sqlalchemy import desc

from .models import Execucao, History, ExecucaoYearInfo
from cuidando_utils import db, ExtraApi

api = ExtraApi(version='1.0',
               title='Gastos Abertos',
               description='API para acesso a dados orçamentários')
# ns = api.namespace('api/v1/execucao', 'Dados sobre execução')

api.update_parser_arguments({
    'code': {
        'type': str,
        'help': 'Code.',
    },
    'codes': {
        'type': list,
        'location': 'json',
        'default': None,
        'help': 'List of codes.',
    },
    'year': {
        'type': int,
        'help': 'Year.',
    },
    'page': {
        'type': int,
        'default': 0,
        'help': 'Page.',
    },
    'per_page_num': {
        'type': int,
        'default': 100,
        'help': 'Number of elements per page.',
    },
    'has_key': {
        'type': str,
        'help': 'Field that must have been modified.',
    },
    'state': {
        'type': bool,
        'help': 'State or not state'
    },
    'capcor': {
        'type': bool,
        'help': 'Capital or Corrente'
    }
})


@api.route('/info')
class ExecucaoInfoApi(Resource):

    def get(self):
        '''Information about all the database (currently only years).'''
        dbyears = db.session.query(Execucao.get_year()).distinct().all()
        years = sorted([i[0] for i in dbyears])

        return {
            'data': {
                'years': years,
            }
        }


@api.route('/info/<int:year>')
class ExecucaoInfoMappedApi(Resource):

    def get(self, year):
        '''Information about a year.'''
        return db.session.query(ExecucaoYearInfo).get(year).data


@api.route('/minlist/<int:year>')
class ExecucaoMinListApi(Resource):

    @api.parsed_args('state', 'capcor')
    def get(self, year, state, capcor):
        '''Basic information about all geolocated values in a year.
        This endpoint is usefull to plot all the points in a map and use the
        codes to get more information about specific points. Using parameters
        it is possible to get more information about all the points. Only codes
        and latlons are returned by default.'''

        fields = filter(lambda i: i is not None, [
            Execucao.code,
            Execucao.point.ST_AsGeoJSON(3),
            Execucao.state if state else None,
            Execucao.cap_cor if capcor else None,
        ])

        items = (
            db.session.query(*fields)
            .filter(Execucao.get_year() == str(year))
            .filter(Execucao.point_found())
            .all())

        return {
            'FeatureColletion': [
                {'type': 'Feature',
                 'properties': dict(filter(lambda i: i[1], (
                     # Add required properties
                     ('uid', v.code),
                     ('state', v.state if state else None),
                     ('cap_cor', v.cap_cor if capcor else None),
                 ))),
                 'geometry': json.loads(v[1])}
                for v in items
            ]
        }


@api.route('/list')
class ExecucaoAPI(Resource):

    @api.parsed_args('code', 'year', 'page', 'per_page_num')
    def get(self, page, per_page_num, code=None, year=None):
        '''List execução data in pages.'''
        execucao_data = query_execucao()

        # Get only row of 'code'
        if code:
            execucao_data = execucao_data.filter(Execucao.code == code)
        # Get all rows of 'year'
        elif year:
            execucao_data = execucao_data.filter(
                Execucao.get_year() == str(year))

        total = execucao_data.count()

        # Limit que number of results per page
        execucao_data = (execucao_data.offset(page*per_page_num)
                         ).limit(per_page_num)

        return data2json(execucao_data.all()), 200, headers_with_counter(total)

    @api.parsed_args('codes')
    def post(self, codes=None):
        '''Return information about a given list of codes.'''
        if codes:
            execucao_data = (query_execucao()
                             .filter(Execucao.code.in_(codes))
                             .all())
        else:
            execucao_data = []
        return data2json(execucao_data)


@api.route('/updates')
class ExecucaoUpdates(Resource):

    @api.parsed_args('page', 'per_page_num', 'has_key')
    def get(self, page, per_page_num, has_key):
        '''Rows updates.'''
        fields = (History, Execucao.data['ds_projeto_atividade'])
        updates_data = (db.session.query(*fields)
                        .order_by(desc(History.date))
                        .filter(Execucao.code == History.code))
        if has_key:
            updates_data = updates_data.filter(History.data.has_key(has_key))  # noqa

        total = updates_data.count()

        # Limit que number of results per page
        updates_data = (updates_data.offset(page*per_page_num)
                        ).limit(per_page_num)

        return {
            'data': [{
                'date': hist.date.strftime('%Y-%m-%d'),
                'event': hist.event,
                'code': hist.code,
                'description': descr,
                'data': hist.data
            } for hist, descr in updates_data.all()]
        }, 200, headers_with_counter(total)


def headers_with_counter(total):
    return {
        # Add 'Access-Control-Expose-Headers' header here is a workaround
        # until Flask-Restful adds support to it.
        'Access-Control-Expose-Headers': 'X-Total-Count',
        'X-Total-Count': total
    }


def query_execucao():
    return db.session.query(Execucao.point.ST_AsGeoJSON(3), Execucao)


def data2json(rows):
    return {'data': [
        dict({
            'code': i[1].code,
            'notification_id': i[1].get_notification_id(),
            'notification_author': current_app.config['VIRALATA_USER'],
            'geometry': json.loads(i[0]) if i[0] else None,
        }, **i[1].data)
        for i in rows
    ]}
