#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals  # unicode by default
import os

from flask import Flask, send_file, send_from_directory
from flask_cors import CORS
from flask_restplus import apidoc
from flask_migrate import Migrate

from extensions import db, sv
from views import api
from browser import ESicLivre


def create_app(settings_folder):
    # App
    app = Flask(__name__)
    Migrate(app, db)
    app.config.from_pyfile('../settings/common.py', silent=False)
    app.config.from_pyfile(
        os.path.join(settings_folder, 'local_settings.py'), silent=False)
    configure_logging(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    # DB
    db.init_app(app)

    # Signer/Verifier
    if app.config.get('PUBLIC_KEY_PATH'):
        pub_key_path = app.config['PUBLIC_KEY_PATH']
    else:
        pub_key_path = os.path.join(settings_folder, 'keypub')
    sv.config(pub_key_path=pub_key_path)

    # Browser
    browser = ESicLivre()
    browser.config(
        firefox=app.config['FIREFOX_PATH'],
        email=app.config['ESIC_EMAIL'],
        senha=app.config['ESIC_PASSWORD'],
        pasta=app.config['DOWNLOADS_PATH'],
        logger=app.logger,
        app=app,
        )
    app.browser = browser

    # API
    api.init_app(app)
    app.register_blueprint(apidoc.apidoc)
    api.browser = browser

    # TODO: colocar isso em um lugar descente...
    @app.route('/static/<path:path>')
    def send_templates(path):
        return send_from_directory('static/', path)

    @app.route('/captcha')
    def send_captcha():
        return send_file('static/captcha.jpg')

    @app.cli.command()
    def browser_once():
        '''Run browser once.'''
        app.browser.rodar_uma_vez()

    return app


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    import logging.handlers

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)
