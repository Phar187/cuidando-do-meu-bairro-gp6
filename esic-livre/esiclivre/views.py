#!/usr/bin/env python
# coding: utf-8

import arrow
import bleach

import sqlalchemy as sa
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import Resource
from flask import current_app
import pandas as pd

from esiclivre.models import Orgao, Author, UserMessage, Pedido, Message, Keyword
from cuidando_utils import db, paginate, ExtraApi


api = ExtraApi(version='1.0',
               title='EsicLivre',
               description='A microservice for eSIC interaction. All non-get '
               'operations require a micro token.')

api.update_parser_arguments({
    'text': {
        'location': 'json',
        'help': 'The text for the pedido.',
    },
    'protocolo': {
        'location': 'json',
        'help': 'The protocolo of the pedido.',
    },
    'orgao': {
        'location': 'json',
        'help': 'Orgao that should receive the pedido.',
    },
    'keywords': {
        'location': 'json',
        'type': list,
        'help': 'Keywords to tag the pedido.',
    },
})


@api.route('/orgaos')
class ListOrgaos(Resource):

    def get(self):
        '''List orgaos.'''
        return {
            "orgaos": [i[0] for i in db.session.query(Orgao.name).all()]
        }


@api.route('/messages')
class MessageApi(Resource):

    @api.parsed_args('page', 'per_page_num')
    def get(self, page, per_page_num):
        '''List messages by decrescent time.'''
        messages = (db.session.query(Pedido, Message)
                    .options(joinedload('keywords'))
                    .filter(Message.pedido_id == Pedido.id)
                    .order_by(desc(Message.date)))
        # Limit que number of results per page
        messages, total = paginate(messages, page, per_page_num)
        return {
            'messages': [
                dict(msg.as_dict, keywords=[kw.name for kw in pedido.keywords])
                for pedido, msg in messages
            ],
            'total': total,
        }


@api.route('/pedidos')
class PedidoApi(Resource):

    @api.parsed_args('token', 'text', 'orgao', 'keywords')
    def post(self, author_name, text, orgao, keywords):
        '''Adds a new pedido to be submited to eSIC.'''

        text = bleach.clean(text, strip=True)

        # Size limit enforced by eSIC
        if len(text) > 6000:
            api.abort_with_msg(400, 'Text size limit exceeded.', ['text'])

        # Validate 'orgao'
        if orgao:
            orgao_exists = db.session.query(Orgao).filter_by(name=orgao).count() == 1
            if not orgao_exists:
                api.abort_with_msg(400, 'Orgao not found.', ['orgao'])
        else:
            api.abort_with_msg(400, 'No Orgao specified.', ['orgao'])

        # Get author (add if needed)
        try:
            author = db.session.query(Author).filter_by(name=author_name).one()
        except NoResultFound:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        pedido = Pedido(author=author, orgao_name=orgao, description=text)
        db.session.add(pedido)

        # get keywords
        for keyword_name in keywords:
            try:
                keyword = db.session.query(Keyword).filter_by(name=keyword_name).one()
            except NoResultFound:
                keyword = Keyword(name=keyword_name)
                db.session.add(keyword)
            pedido.keywords.append(keyword)

        pergunta = UserMessage(
            author_id=author.id, pedido_id=pedido.id, orgao_name=orgao,
            # keywords=','.join(k for k in keywords),
            text=text, created_at=arrow.now(),
            state=UserMessage.states.waiting,
            type=UserMessage.types.pergunta)

        db.session.add(pergunta)
        db.session.commit()
        return {
            'status': 'ok',
            'subscribe_data': {
                'id': pedido.get_notification_id(),
                'author': current_app.config['VIRALATA_USER']}}


@api.route('/recurso/<int:protocolo>')
class RecursoApi(Resource):

    @api.parsed_args('token', 'text')
    def post(self, author_name, protocolo, text):
        '''Adds a new recurso to be submited to eSIC.'''

        text = bleach.clean(text, strip=True)

        # Size limit enforced by eSIC
        if len(text) > 6000:
            api.abort_with_msg(400, 'Text size limit exceeded.', ['text'])

        # Get author (add if needed)
        try:
            author = db.session.query(Author.id).filter_by(name=author_name).one()
        except NoResultFound:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        try:
            pedido = db.session.query(Pedido).filter_by(protocol=protocolo).one()
        except NoResultFound:
            api.abort(404, 'Pedido not found')

        if pedido.author != author:
            api.abort(403, 'Only the author of pedido can add recurso.')

        if not pedido.allow_recurso:
            api.abort(403, 'Recurso not allowed at the moment.')

        recurso = UserMessage(
            pedido_id=pedido.id,
            state=UserMessage.states.waiting,
            text=text, author_id=author.id,
            created_at=arrow.now())
        db.session.add(recurso)
        pedido.allow_recurso = False
        db.session.commit()
        return {'status': 'ok'}


@api.route('/pedidos/protocolo/<int:protocolo>')
class GetPedidoProtocolo(Resource):

    def get(self, protocolo):
        '''Returns a pedido by its protocolo.'''
        try:
            pedido = (db.session.query(Pedido)
                      .options(joinedload('history'))
                      .options(joinedload('keywords'))
                      .filter_by(protocol=protocolo).one())
        except NoResultFound:
            api.abort(404)
        return pedido.as_dict


@api.route('/pedidos/id/<int:id_number>')
class GetPedidoId(Resource):

    def get(self, id_number):
        '''Returns a pedido by its id.'''
        try:
            pedido = db.session.query(Pedido).filter_by(id=id_number).one()
        except NoResultFound:
            api.abort(404)
        return pedido.as_dict


@api.route('/keywords/<string:keyword_name>')
class GetPedidoKeyword(Resource):

    def get(self, keyword_name):
        '''Returns pedidos marked with a specific keyword.'''
        try:
            pedidos = (
                db.session.query(Keyword)
                .options(
                    joinedload('pedidos')
                    .joinedload('history'))
                .filter_by(name=keyword_name).one()).pedidos
        except NoResultFound:
            pedidos = []

        sent_pedidos = []
        unsent_pedidos = []
        for p in pedidos:
            if p.request_date:
                sent_pedidos.append(p)
            else:
                unsent_pedidos.append(p)
        sent_pedidos = sorted(sent_pedidos, key=lambda p: p.request_date, reverse=True)
        return {
            'keyword': keyword_name,
            'pedidos': [pedido.as_dict for pedido in unsent_pedidos + sent_pedidos],
            # 'prepedidos': [p for p in list_all_user_messages()
            #                if keyword_name in p['keywords']],
        }


@api.route('/pedidos/orgao/<string:orgao>')
class GetPedidoOrgao(Resource):

    def get(self, orgao):
        try:
            pedido = db.session.query(Pedido).filter_by(orgao=orgao).one()
        except NoResultFound:
            api.abort(404)
        return pedido.as_dict


@api.route('/keywords')
class ListKeywords(Resource):

    def get(self):
        '''List keywords.'''
        keywords = db.session.query(Keyword.name).all()

        return {
            "keywords": [k[0] for k in keywords]
        }


@api.route('/authors/<string:name>')
class GetAuthor(Resource):

    def get(self, name):
        '''Returns pedidos made by an author.'''
        try:
            author = (
                db.session.query(Author)
                .options(
                    joinedload('pedidos', innerjoin=True)
                    .joinedload('keywords', innerjoin=True))
                .filter_by(name=name).one())
        except NoResultFound:
            api.abort(404, 'No pedido for this author.')
        return {
            'name': author.name,
            'pedidos': [
                {
                    'id': p.id,
                    'protocolo': p.protocol,
                    'orgao': p.orgao_name,
                    'situacao': p.situation,
                    'notification_id': p.get_notification_id(),
                    'deadline': p.deadline.isoformat() if p.deadline else '',
                    'keywords': [kw.name for kw in p.keywords],
                }
                for p in author.pedidos
            ]
        }


@api.route('/authors')
class ListAuthors(Resource):

    def get(self):
        '''List authors.'''
        authors = db.session.query(Author.name).all()

        return {
            "authors": [a[0] for a in authors]
        }


@api.route('/waiting')
class UserMessagesAPI(Resource):

    def get(self):
        '''List UserMessages.'''
        return {'waiting': list_all_user_messages()}


def list_all_user_messages():
    q = db.session.query(UserMessage, Author).filter_by(state=UserMessage.states.waiting)
    q = q.filter(UserMessage.author_id == Author.id)

    return [{
        'text': p.text,
        'orgao': p.orgao_name,
        'created': p.created_at.isoformat(),
        'keywords': p.keywords,
        'author': a.name,
    } for p, a in q.all()]


@api.route('/stats/<string:grouping>')
class StatisticsAPI(Resource):

    def get(self, grouping='day'):
        '''Statistics about pedidos.'''

        groups = {
            'day': 'D',
            'month': 'MS',
            'year': 'YS'
        }

        if grouping not in groups:
            api.abort(404)

        by_orgao = (
            db.session.query(
                Pedido.orgao_name, sa.func.count(Pedido.orgao_name))
            .filter(Pedido.orgao_name.isnot(None))
            .group_by(Pedido.orgao_name)
            .all())
        by_orgao = [{
            'name': i[0],
            'count': i[1]
        } for i in by_orgao]
        by_orgao.sort(key=lambda i: i['count'], reverse=True)

        pedidos = db.session.query(Pedido).options(joinedload('history')).all()
        df = pd.DataFrame(
            [(i.history[0].date.datetime, i) for i in pedidos if i.history],
            columns=['date', 'pedido'])
        dates = (
            df.groupby(pd.Grouper(key='date', freq=groups[grouping]))
            .count().reset_index()
            .assign(date=lambda x: (x.date.astype(int) / 1e6).astype(int))
            .values.tolist())

        return {
            'orgaos': by_orgao,
            'dates': dates
        }
