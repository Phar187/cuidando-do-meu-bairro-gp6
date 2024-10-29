from flask import current_app

from cuidando_utils import scape_template, send_notification_messages, db

from .models import History


def send_update_notifications():
    # a=db.session.query(History).order_by(History.id.desc()).limit(10000).all()
    # for i in a:
    #     i.notification_sent=False

    events = db.session.query(History).filter_by(notification_sent=False).options(
                    db.joinedload(History.execucao, innerjoin=True)).all()
    notifications = []
    print(f'Sending {len(events)} notifications...')
    for event in events:
        # Prepare notification message
        try:
            changes = scape_template('\n'.join([
                    f' {k}:\nde "{v[0]}" para "{v[1]}"'
                    for k, v in event.data.items()]))
        except KeyError:
            print('Error to parse changes: ', event.data)
            changes = ''
        text_template = current_app.config['NOTIFICATION_TEMPLATE'].format(
            description=scape_template(
                event.execucao.data.get('ds_projeto_atividade', '')),
            changes=changes
        )
        notifications.append({
            'title': current_app.config['NOTIFICATION_TITLE'],
            'template': text_template,
            'tags': [event.execucao.get_notification_id()]
        })
        event.notification_sent = True

    send_notification_messages(notifications)
    db.session.commit()
