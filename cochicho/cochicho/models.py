#!/usr/bin/env python
# coding: utf-8

import enum
import string

import arrow
import sqlalchemy as sa
from sqlalchemy_utils import ArrowType
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound

from cuidando_utils import date_to_json, db


class Status(enum.Enum):
    unsent = 1
    sent = 2


message_tag = sa.Table(
    'message_tag', db.metadata,
    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Subscription(db.Model):
    __tablename__ = 'subscription'
    subscriber_id = db.Column(
        db.Integer, db.ForeignKey('subscriber.id'), primary_key=True)
    subscriber = db.relationship('Subscriber', backref='subscriptions')
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    tag = db.relationship('Tag', backref='subscriptions')
    # Author allowed to send messages to the subscriber in this subscription
    author = db.Column(db.String(255), nullable=True)
    template_data = db.Column(postgresql.JSONB)

    def as_dict(self):
        return {
            'subscriber': self.subscriber.name,
            'tag': self.tag.name,
            'author': self.author,
            'template_data': self.template_data,
        }


class Subscriber(db.Model):
    __tablename__ = 'subscriber'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)

    @classmethod
    def get_or_create(cls, name):
        try:
            subscriber = db.session.query(cls).filter(cls.name == name).one()
        except NoResultFound:
            subscriber = cls(name=name)
            db.session.add(subscriber)
            db.session.commit()
        return subscriber


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)

    @classmethod
    def get_or_create(cls, name):
        try:
            tag = db.session.query(cls).filter(cls.name == name).one()
        except NoResultFound:
            tag = cls(name=name)
            db.session.add(tag)
            db.session.commit()
        return tag


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status))
    created_at = db.Column(ArrowType, nullable=False)
    sent_at = db.Column(ArrowType, nullable=True)
    author = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    template = db.Column(sa.UnicodeText())
    destinations = db.relationship('Tag', secondary=message_tag, backref='messages')

    @classmethod
    def create_if_subscribed(cls, author, messages):
        '''Create a message to be sent, only if destinations have subscribers.'''
        messages_tags = list(set(tag for msg in messages for tag in msg['tags']))
        subscribed_tags = (
            db.session.query(Tag)
            # Return only tags that will be used in this method call
            .filter(Tag.name.in_(messages_tags))
            # Select tags only with subscribers
            .filter(Tag.subscriptions.any())
            .all())

        # Organize by tag name
        subscribed_tags = {tag.name: tag for tag in subscribed_tags}

        for message in messages:
            tags = message['tags']
            title = message['title']
            template = message['template']
            if tags:
                message = cls(
                    created_at=arrow.now(), status=Status.unsent, author=author,
                    template=template, title=title)
                # add destination tags
                for tag in tags:
                    tag = subscribed_tags.get(tag)
                    if tag:
                        message.destinations.append(tag)
                        db.session.add(message)
        db.session.commit()

    def as_dict(self, template_data):
        return {
            'status': self.status.name,
            'destinations': [tag.name for tag in self.destinations],
            'author': self.author,
            'title': self.title,
            'created': date_to_json(self.created_at),
            'sent': date_to_json(self.sent_at),
            'body': self.format_body(template_data),
        }

    def format_body(self, data):
        '''Format the message body using its template and a template data dict.'''
        # return self.template.format(**data)
        return string.Template(self.template).safe_substitute(**data)
