# -*- coding: utf-8 -*-

import os

# from flask import Flask, request, render_template
# from flask.ext.babel import Babel
# from flask.ext.restful.utils import cors
# from flask.ext.cors import CORS
# from flask_restplus import apidoc

import cuidando_utils
# from .config import DefaultConfig, INSTANCE_FOLDER_PATH
# from .extensions import db, api
# from .execucao import execucao
from .views import api
from .data_import import update_execucao
from .sender import send_update_notifications


# DEFAULT_BLUEPRINTS = (
#     execucao,
# )


def create_app(settings_folder):
    """Create a Flask app."""
    app = cuidando_utils.create_app(settings_folder, api, init_sv='public')

    # if app_name is None:
    #     app_name = DefaultConfig.PROJECT
    # # if blueprints is None:
    # #     blueprints = DEFAULT_BLUEPRINTS
    # if instance_folder is None:
    #     instance_folder = INSTANCE_FOLDER_PATH

    # app = Flask(__name__, instance_path=instance_folder,
    #             instance_relative_config=True)
    # configure_app(app, config)
    # # configure_hook(app)
    # configure_blueprints(app, blueprints)
    # configure_extensions(app)
    # # configure_logging(app)
    # configure_error_handlers(app)

    # # Full CORS!
    # CORS(app, resources={r"*": {"origins": "*"}})

    @app.cli.command()
    def update_data():
        '''Download and import Execucao data.'''
        update_execucao.update(
            app.db,
            app.config['STORAGE_FOLDER'],
            app.config['PUBLIC_DOWNLOADS_FOLDER'])

    @app.cli.command()
    def send_notifications():
        '''Send notifications about Execucao updates.'''
        send_update_notifications()

    return app


# def configure_app(app, config=None):
#     """Different ways of configurations."""

#     # http://flask.pocoo.org/docs/api/#configuration
#     app.config.from_object(DefaultConfig)

#     # Allows setting config from outsite instance folder
#     non_instance_config = os.path.join(
#         os.path.dirname(app.root_path), 'settings', 'local_settings.py')
#     app.config.from_pyfile(non_instance_config, silent=True)

#     # http://flask.pocoo.org/docs/config/#instance-folders
#     instance_config = os.path.join(
#         app.config.get('INSTANCE_FOLDER_PATH', ''), 'production.cfg')
#     app.config.from_pyfile(instance_config, silent=True)

#     if config:
#         app.config.from_object(config)

    # Use instance folder instead of env variables to make deployment easier.
    # app.config.from_envvar('%s_APP_CONFIG' % DefaultConfig.PROJECT.upper(), silent=True)


# def configure_extensions(app):
#     # flask-sqlalchemy
#     db.init_app(app)

#     # flask-babel
#     babel = Babel(app)

#     @babel.localeselector
#     def get_locale():
#         accept_languages = app.config.get('ACCEPT_LANGUAGES')
#         return request.accept_languages.best_match(accept_languages)


# def configure_blueprints(app, blueprints):
#     """Configure blueprints in views."""

#     for blueprint in blueprints:
#         app.register_blueprint(blueprint)


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging

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


# def configure_error_handlers(app):

#     @app.errorhandler(403)
#     def forbidden_page(error):
#         return render_template("errors/forbidden_page.html"), 403

#     @app.errorhandler(404)
#     def page_not_found(error):
#         return render_template("errors/page_not_found.html"), 404

#     @app.errorhandler(500)
#     def server_error_page(error):
#         return render_template("errors/server_error.html"), 500
