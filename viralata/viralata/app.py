#!/usr/bin/env python
# coding: utf-8

from flask_mail import Mail

import cuidando_utils
from viralata.views import api
# from viralata.auths import init_social_models


def create_app(settings_folder):
    app = cuidando_utils.create_app(settings_folder, api, init_sv='private')

    # Social
    # init_social_models(app)

    # Mail
    api.mail = Mail(app)

    return app
