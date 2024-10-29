import os

from flask import current_app
import flask_mail

import cuidando_utils
from cuidando_utils import db

from .models import Message, Status, Tag, Subscription


def send_all(api):
    '''Send all messages waiting to be sent.'''
    messages = (db.session.query(Message)
                .options(
                    db.joinedload(Message.destinations, innerjoin=True)
                    .joinedload(Tag.subscriptions, innerjoin=True)
                    .joinedload(Subscription.subscriber, innerjoin=True))
                .filter_by(status=Status.unsent).all())

    # Get data about emails that should be sent
    emails_data = []
    for message in messages:
        for tag in message.destinations:
            for subscription in tag.subscriptions:
                if message.author == subscription.author:
                    emails_data.append({
                        'message': message,
                        'dest': subscription.subscriber.name,  # username, not email
                        'template_data': subscription.template_data
                    })

    usernames = list(set(i['dest'] for i in emails_data))
    users_emails = get_subscribers_emails(usernames)
    # Replace usernames with real emails addresses
    for email_data in emails_data[:]:
        username = email_data['dest']
        user = users_emails.get(username)
        if user:
            email_data['dest'] = user['email']
        else:
            emails_data.remove(email_data)
            print('User not found in Viralata:', username)

    print(f'Sending {len(emails_data)} emails...')

    # Send e-mails
    if emails_data:
        with current_app.mail.connect() as conn:
            for email_data in emails_data:
                send_message(conn, current_app.config['SENDER_NAME'], **email_data)
                email_data['message'].status = Status.sent
                db.session.commit()


def send_message(conn, sender, message, dest, template_data):
    '''Send an email message.'''
    mail_msg = flask_mail.Message(
        subject=message.title,
        sender=sender,
        recipients=[dest],
        body=message.format_body(template_data)
    )
    conn.send(mail_msg)


def get_subscribers_emails(subscribers):
    endpoint = os.path.join(current_app.config['VIRALATA_ADDRESS'], 'users')
    return cuidando_utils.request('get', endpoint, {'users': subscribers})['users']
