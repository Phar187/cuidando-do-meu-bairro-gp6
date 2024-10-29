#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals  # unicode by default
import json

# import arrow
# import bleach
# from sqlalchemy import desc
from flask_restplus import Resource
import sqlalchemy as sa

from cuidando_utils import ExtraApi, db

from cochicho.models import Subscriber, Tag, Subscription, Message


api = ExtraApi(
    version='1.0',
    title='Cochicho',
    description='A notification microservice.')

api.update_parser_arguments({
    'subscriber': {
        'location': 'json',
        'help': 'Subscriber name.',
    },
    'tag': {
        'location': 'json',
        'help': 'Tag name.',
    },
    'tags': {
        'location': 'json',
        'type': list,
        'help': 'Tags name list.',
        'required': True,
    },
    'messages': {
        'location': 'json',
        'type': list,
        'help': 'Messages list.',
        'required': True,
    },
    'subscriptions': {
        'location': 'json',
        'type': list,
        'help': 'Subscriptions.',
        'required': True,
    },
})


def clear_template_data(data):
    '''Make checks to template data to avoid exploitations.'''
    if len(json.dumps(data)) > 2**15:
        raise 'too big'
    return data


@api.route('/subscriptions')
class SubscriptionsAPI(Resource):

    @api.parsed_args('subscriber', 'tag')
    def post(self, subscriber=None, tag=None):
        '''Get subscriptions filtering by subscriber and tag.'''
        # TODO: better doc, or change method
        q = db.session.query(Subscription)
        if subscriber:
            q = q.filter(Subscription.subscriber.has(name=subscriber))
        elif tag:
            q = q.filter(Subscription.tag.has(name=tag))
        else:
            return {'subscriptions': []}
        return {'subscriptions': [i.as_dict() for i in q.all()]}

    @api.parsed_args('token', 'subscriptions')
    def put(self, subscriber_name, subscriptions):
        '''Subscribe to receive notifications about tags.
        Receives a list of objects in this format:
            author: str (allowed to send notifications)
            tag: str (tag to which subscribe)
            template_data: dict (used in the message)
        '''
        subscriber = Subscriber.get_or_create(subscriber_name)
        for subscription_data in subscriptions:
            tag_name = subscription_data['tag']
            template_data = subscription_data.get('template_data', {})
            author = subscription_data['author']
            tag = Tag.get_or_create(tag_name)
            subscription = Subscription(
                tag_id=tag.id, subscriber_id=subscriber.id, author=author,
                template_data=clear_template_data(template_data))
            db.session.add(subscription)
        try:
            db.session.commit()
        except sa.exc.IntegrityError:
            db.session.rollback()
            api.abort(400, 'Maybe already subscribed?')
        return {'status': 'ok'}

    @api.parsed_args('token', 'tags')
    def delete(self, subscriber_name, tags):
        '''Delete subscriptions to tags.
        Returns ok even when no subscriptions are found.'''
        (db.session.query(Subscription)
         .filter(Subscription.subscriber.has(name=subscriber_name))
         .filter(Subscription.tag.has(Tag.name.in_(tags)))
         .delete(synchronize_session=False))
        # subscriptions = (
        #     db.session.query(Subscription)
        #     .filter(Subscription.subscriber.has(name=subscriber_name))
        #     .filter(Subscription.tag.has(Tag.name.in_(tags)))
        #     .all())
        # for subscription in subscriptions:
        #     db.session.delete(subscription)
        db.session.commit()
        return {'status': 'ok'}


@api.route('/messages')
class MessagesAPI(Resource):

    @api.parsed_args('token')
    def post(self, subscriber_name):
        '''Get messages destinated to a subscriber.'''
        subscriptions = (
            db.session.query(Subscription)
            .options(
                db.joinedload(Subscription.tag, innerjoin=True)
                .joinedload(Tag.messages, innerjoin=True))
            .filter(Subscription.subscriber.has(name=subscriber_name))).all()
        messages = []
        for subscription in subscriptions:
            for message in subscription.tag.messages:
                messages.append(message.as_dict(subscription.template_data))
        return {'messages': messages}

    @api.parsed_args('token', 'messages')
    def put(self, author_name, messages):
        '''A list of messages to be sent to subscribers.

        title: str
        template: str
        tags: [str] (destination tags)

        Template uses: https://docs.python.org/3.6/library/string.html#template-strings
        '''
        Message.create_if_subscribed(author_name, messages)
        return {'status': 'ok'}
