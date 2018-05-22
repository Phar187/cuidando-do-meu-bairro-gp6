#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals  # unicode by default

from multiprocessing import Process

import arrow
import bleach
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from flask_restplus import Resource

from viralata.utils import decode_token
from cutils import paginate, ExtraApi

from models import Orgao, Author, PrePedido, Pedido, Message, Keyword
from extensions import db, sv


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


@api.route('/captcha/<string:value>')
class SetCaptcha(Resource):

    def get(self, value):
        '''Sets a captcha to be tried by the browser.'''
        process = Process(target=set_captcha_func, args=(value,))
        process.start()
        return {}


@api.route('/messages')
class MessageApi(Resource):

    @api.doc(parser=api.create_parser('page', 'per_page_num'))
    def get(self):
        '''List messages by decrescent time.'''
        args = api.general_parse()
        page = args['page']
        per_page_num = args['per_page_num']
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

    @api.doc(parser=api.create_parser('token', 'text', 'orgao', 'keywords'))
    def post(self):
        '''Adds a new pedido to be submited to eSIC.'''
        args = api.general_parse()
        decoded = decode_token(args['token'], sv, api)
        author_name = decoded['username']

        text = bleach.clean(args['text'], strip=True)

        # Size limit enforced by eSIC
        if len(text) > 6000:
            api.abort_with_msg(400, 'Text size limit exceeded.', ['text'])

        # Validate 'orgao'
        if args['orgao']:
            orgao_exists = db.session.query(Orgao).filter_by(
                name=args['orgao']).count() == 1
            if not orgao_exists:
                api.abort_with_msg(400, 'Orgao not found.', ['orgao'])
        else:
            api.abort_with_msg(400, 'No Orgao specified.', ['orgao'])

        # Get author (add if needed)
        try:
            author_id = db.session.query(
                Author.id).filter_by(name=author_name).one()
        except NoResultFound:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
            author_id = author.id

        # get keywords
        for keyword_name in args['keywords']:
            try:
                keyword = (db.session.query(Keyword)
                           .filter_by(name=keyword_name).one())
            except NoResultFound:
                keyword = Keyword(name=keyword_name)
                db.session.add(keyword)
                db.session.commit()

        pre_pedido = PrePedido(
            author_id=author_id, orgao_name=args['orgao'],
            keywords=','.join(k for k in args['keywords']),
            text=text, state='WAITING', created_at=arrow.now())

        db.session.add(pre_pedido)
        db.session.commit()
        return {'status': 'ok'}


@api.route('/recurso/<int:protocolo>')
class RecursoApi(Resource):

    @api.doc(parser=api.create_parser('token', 'text'))
    def post(self, protocolo):
        '''Adds a new recurso to be submited to eSIC.'''
        args = api.general_parse()
        # decoded = decode_token(args['token'], sv, api)
        # author_name = decoded['username']
        # TODO: TIRARRRRRRRRRRR!
        author_name = 'abacate'

        text = bleach.clean(args['text'], strip=True)

        # Size limit enforced by eSIC
        if len(text) > 6000:
            api.abort_with_msg(400, 'Text size limit exceeded.', ['text'])

        # Get author (add if needed)
        try:
            author_id = db.session.query(
                Author.id).filter_by(name=author_name).one()
        except NoResultFound:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
            author_id = author.id

        try:
            pedido = db.session.query(Pedido).filter_by(protocol=protocolo).one()
        except NoResultFound:
            api.abort(404, 'Pedido not found')

        if pedido.author.id != author_id:
            api.abort(403, 'Only the author of pedido can add recurso')

        pre_pedido = PrePedido(
            pedido_id=pedido.id, state='WAITING', text=text, author_id=author_id,
            created_at=arrow.now())
        db.session.add(pre_pedido)
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


# @api.route('/recursos/protocolo/<int:protocolo>')
# class GetRecursoProtocolo(Resource):

#     def get(self, protocolo):
#         '''Returns a recurso by its pedido protocolo.'''
#         try:
#             recurso = (db.session.query(Recurso)
#                       .filter_by(protocol=protocolo).one())
#         except NoResultFound:
#             api.abort(404)
#         return recurso.as_dict


@api.route('/pedidos/id/<int:id_number>')
class GetPedidoId(Resource):

    def get(self, id_number):
        '''Returns a pedido by its id.'''
        try:
            pedido = db.session.query(Pedido).filter_by(id=id_number).one()
        except NoResultFound:
            api.abort(404)
        return pedido.as_dict


# @api.route('/recursos/id/<int:id_number>')
# class GetRecursoId(Resource):

#     def get(self, id_number):
#         '''Returns a Recurso by its pedido id.'''
#         try:
#             recurso = db.session.query(Recurso).filter_by(pedido_id=id_number).one()
#         except NoResultFound:
#             api.abort(404)
#         return recurso.as_dict


@api.route('/keywords/<string:keyword_name>')
class GetPedidoKeyword(Resource):

    def get(self, keyword_name):
        '''Returns pedidos marked with a specific keyword.'''
        try:
            pedidos = (db.session.query(Keyword)
                       .options(joinedload('pedidos'))
                       .options(joinedload('pedidos.history'))
                       .filter_by(name=keyword_name).one()).pedidos
        except NoResultFound:
            pedidos = []
        return {
            'keyword': keyword_name,
            'pedidos': [
                pedido.as_dict for pedido in sorted(
                    pedidos, key=lambda p: p.request_date, reverse=True
                )
            ],
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
            author = (db.session.query(Author)
                      .options(joinedload('pedidos'))
                      .filter_by(name=name).one())
        except NoResultFound:
            api.abort(404)
        return {
            'name': author.name,
            'pedidos': [
                {
                    'id': p.id,
                    'protocolo': p.protocol,
                    'orgao': p.orgao_name,
                    'situacao': p.situation,
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


@api.route('/prepedidos')
class PrePedidoAPI(Resource):

    def get(self):
        '''List PrePedidos.'''
        return {'prepedidos': list_all_prepedidos()}


def list_all_prepedidos():
    q = db.session.query(PrePedido, Author).filter_by(state='WAITING')
    q = q.filter(PrePedido.author_id == Author.id)

    return [{
        'text': p.text,
        'orgao': p.orgao_name,
        'created': p.created_at.isoformat(),
        'keywords': p.keywords,
        # 'tipo': p.tipo,
        'author': a.name,
    } for p, a in q.all()]


def set_captcha_func(value):
    '''Sets a captcha to be tried by the browser.'''
    api.browser.set_captcha(value)
