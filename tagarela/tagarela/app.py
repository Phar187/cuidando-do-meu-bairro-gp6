#!/usr/bin/env python
# coding: utf-8

from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

import cuidando_utils
from tagarela.views import api


def create_app(settings_folder):
    app = cuidando_utils.create_app(settings_folder, api, init_sv='public')

    # Mail
    api.mail = Mail(app)

    api.urltoken = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    return app
