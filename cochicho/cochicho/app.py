#!/usr/bin/env python
# coding: utf-8

from flask_mail import Mail

import cuidando_utils

from .views import api
from .sender import send_all


def create_app(settings_folder):
    app = cuidando_utils.create_app(settings_folder, api, init_sv='public')

    # Mail
    app.mail = Mail(app)

    @app.cli.command()
    def send_messages():
        '''Send all messages.'''
        send_all(api)

    return app
