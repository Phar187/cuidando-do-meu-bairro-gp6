#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound

from flask.ext.restplus import Resource, Api, apidoc

from models import Comment, Thread, Author
from extensions import db, sv


api = Api(version='1.0',
          title='comments',
          description='Comments')


parser = api.parser()
parser.add_argument('token', location='json')
parser.add_argument('text', location='json')
# From http cookies
# parser.add_argument('session_id', location='cookies')


@api.route('/<string:thread_name>/add')
class AddComment(Resource):

    def post(self, thread_name):
        args = parser.parse_args()
        try:
            decoded = sv.decode(args['token'])
        except:
            # TODO: tratar erros...
            raise
        author_name = decoded['username']

        # TODO: validar text (XSS)
        text = args['text']

        # Get thread (add if needed)
        try:
            thread_id = (db.session.query(Thread.id)
                         .filter(Thread.name == thread_name).one())
        except NoResultFound:
            thread = Thread(name=thread_name)
            db.session.add(thread)
            db.session.commit()
            thread_id = thread.id

        # Get author (add if needed)
        try:
            author_id = (db.session.query(Author.id)
                         .filter(Author.name == author_name).one())
        except NoResultFound:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
            author_id = author.id

        now = datetime.now()
        comment = Comment(author_id=author_id, text=text, thread_id=thread_id,
                          created=now, modified=now)
        db.session.add(comment)
        db.session.commit()
        return {}


@api.route('/<string:thread_name>/<int:comment>/delete')
class DeleteComment(Resource):

    def delete(self, thread_name, comment):
        pass


@api.route('/<string:thread_name>/<int:comment>/edit')
class EditComment(Resource):

    def put(self, thread_name, comment):
        pass


@api.route('/<string:thread_name>')
class GetThread(Resource):

    def get(self, thread_name):
        try:
            thread = (db.session.query(Thread)
                      .filter(Thread.name == thread_name).one())
        except NoResultFound:
            api.abort(404)
        return {
            "list": [
                {
                    "id": c.id,
                    "text": c.text,
                    "author": c.author.name,
                    "created": str(c.created),
                    "modified": str(c.modified),
                }
                for c in thread.comments
            ]
        }


# @api.route('/<string:thread_name>/<int:comment>')
# class GetComment(Resource):

#     def get(self, thread_name, comment):
#         pass
