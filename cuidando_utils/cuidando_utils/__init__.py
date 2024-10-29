#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals  # unicode by default
import os
import datetime
import json
from functools import wraps

import jwt
import requests
from flask import Flask, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restplus import Api, apidoc
from flask_sqlalchemy import SQLAlchemy
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend

from .auth import register, get_token
# from cryptography.x509 import load_pem_x509_certificate

# openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout privateKey.key -out certificate.crt
# cert_obj = load_pem_x509_certificate(cert_str, default_backend())
# cert_obj.public_key()
# serialization.load_ssh_public_key(r, d)


class SignerVerifier(object):
    '''Class to encode and decode JWTs.'''

    def __init__(self, **kwargs):
        self.defaults = {
            'priv_key_path': None,
            'priv_key_password': None,
            'pub_key_path': None,
            'algorithm': 'RS512',
            'options': {
                'require_exp': True,
            }
        }
        self.config(init_defaults=True, **kwargs)

    def config(self, init_defaults=False, **kwargs):
        '''Configures this class, loading defaults if asked, and then the passed
        args.'''

        # Init defaults
        if init_defaults:
            for k, v in self.defaults.items():
                setattr(self, k, v)

        # Use passed args
        for k, v in kwargs.items():
            if k in self.defaults:
                setattr(self, k, v)
            else:
                raise 'Error! Unknown arg!: ' + k

        if 'priv_key_path' in kwargs:
            self.load_priv_key(self.priv_key_path, self.priv_key_password)
        if 'pub_key_path' in kwargs:
            self.load_pub_key(self.pub_key_path)

    def load_priv_key(self, path, priv_key_password=None):
        '''Loads private and public key from a private key PEM file.'''
        with open(path, 'rb') as key_file:
            self.priv_key = load_pem_private_key(key_file.read(),
                                                 priv_key_password,
                                                 default_backend())
            self.pub_key = self.priv_key.public_key()

    def load_pub_key(self, path):
        '''Loads public key from a public key SSH file.'''
        with open(path, 'r') as key_file:
            self.pub_key = key_file.read()

    def encode(self, data, exp_minutes=5):
        '''Encodes data. If has 'exp', sets expiration to it.'''
        if self.priv_key:
            data['exp'] = (datetime.datetime.utcnow() +
                           datetime.timedelta(minutes=exp_minutes))
            return jwt.encode(
                data,
                self.priv_key,
                algorithm=self.algorithm
            ).decode('utf8')
        else:
            raise 'Error: No private key!'

    def decode(self, data):
        '''Decodes data.'''
        if self.pub_key:
            return jwt.decode(data, self.pub_key, options=self.options)
        else:
            raise 'Error: No public key!'


def paginate(query, page, per_page_num):
    '''Paginate a query, returning also the total before pagination.'''
    total = query.count()
    return (query.offset(page*per_page_num).limit(per_page_num).all(), total)


def date_to_json(date):
    '''Helper to format dates.'''
    return str(date)


class ExtraApi(Api):

    def __init__(self, *args, **kwargs):
        super(ExtraApi, self).__init__(*args, **kwargs)
        self.parser_arguments = {
            'token': {
                'location': 'json',
                'help': 'The authentication token.',
                'required': True
            },
            'optional_token': {
                'location': 'json',
                'help': 'Optional authentication token.',
                # 'dest': 'token',
                'required': False
            },
            'page': {
                'type': int,
                'default': 0,
                'help': 'Page to be returned.',
            },
            'per_page_num': {
                'type': int,
                'default': 20,
                'help': 'Number of items per page.',
            },
        }
        self.update_general_parser()

    def init_app(self, app):
        super().init_app(app)

        @app.cli.command()
        def reset_db():
            '''Clear the existing data and create new tables.'''
            db.drop_all()
            db.create_all()

        @app.cli.command()
        def create_db():
            '''Create new tables.'''
            db.create_all()

        @app.cli.command()
        def register_viralata_user():
            '''Register a user in a Viralata instance.'''
            register()

    def update_general_parser(self):
        '''Create a new general parser with current parser_arguments.'''
        self.general_parser = self.create_parser(*self.parser_arguments)

    def update_parser_arguments(self, arguments):
        '''Updates the parser_arguments and recreates the general_parser.'''
        self.parser_arguments.update(arguments)
        self.update_general_parser()

    def create_parser(self, *args):
        '''Create a parser for the passed arguments.'''
        parser = self.parser()
        for arg in args:
            parser.add_argument(arg, **self.parser_arguments[arg])
        return parser

    def general_parse(self):
        '''Parse arguments using any arguments from parser_argumentsar.'''
        return self.general_parser.parse_args()

    def parsed_args(self, *args, parse_token=True):
        '''Use this function as a decorator.'''
        parser = self.create_parser(*args)

        def real_decorator(function):
            @wraps(function)
            @self.doc(parser=parser)
            def wrapper(*args, **kw):
                args_json = parser.parse_args()
                if parse_token and 'token' in args_json:
                    token = args_json.pop('token')
                    username = self.decode_token(token)['username']
                    return function(self, username, **args_json, **kw)
                elif parse_token and 'optional_token' in args_json:
                    token = args_json.pop('optional_token')
                    if token:
                        username = self.decode_token(token)['username']
                    else:
                        username = None
                    return function(self, username, **args_json, **kw)
                else:
                    return function(self, **args_json, **kw)
            return wrapper

        return real_decorator

    def abort_with_msg(self, error_code, msg, fields):
        '''Aborts sending information about the error.'''
        self.abort(error_code, json.dumps({
            'message': msg,
            'fields': fields
        }))

    def decode_validate_token(self, token):
        '''This tries to be a general function to decode and validade any token.
        Receives a token, a SignerVerifier and an API.
        '''
        if not token:
            self.abort(400, 'Error: No token received!')
        try:
            decoded = current_app.sv.decode(token)
            # options={'verify_exp': False})
        except jwt.ExpiredSignatureError:
            self.abort(400, 'Error: Expired token!')
        except jwt.DecodeError:
            self.abort(400, 'Error: Token decode error!')

        # Verify if token has all fields
        for fields in ['username', 'type', 'exp']:
            if fields not in decoded.keys():
                self.abort(400, 'Error: Malformed token! No: %s' % fields)

        return decoded

    def decode_token(self, token):
        '''This function tries to decode and valitade a token used by a client micro
        service. A client micro service is anyone without knowlegde of revoked main
        tokens. Because of this, they should only accept micro tokens.'''
        decoded = self.decode_validate_token(token)
        # TODO: DESCOMENTAR!!!!!!
        # if decoded['type'] != 'micro':
        #     self.abort(400, "Error: This is not a micro token!")
        return decoded


db = SQLAlchemy()
sv = SignerVerifier()


def create_app(settings_folder, api, init_sv=False):
    # App
    app = Flask(__name__)
    app.config.from_pyfile(
        os.path.join(settings_folder, 'common.py'), silent=False)
    app.config.from_pyfile(
        os.path.join(settings_folder, 'local_settings.py'), silent=False)
    CORS(app, resources={r"*": {"origins": "*"}})

    # DB
    db.init_app(app)
    app.db = db
    Migrate(app, db)

    # Signer/Verifier
    if init_sv == 'public':
        # Use public key
        if app.config.get('PUBLIC_KEY_PATH'):
            pub_key_path = app.config['PUBLIC_KEY_PATH']
        else:
            pub_key_path = os.path.join(settings_folder, 'keypub')
        sv.config(pub_key_path=pub_key_path)
        app.sv = sv
    elif init_sv == 'private':
        # Use private key
        sv.config(priv_key_path=os.path.join(settings_folder, 'key'),
                  priv_key_password=app.config['PRIVATE_KEY_PASSWORD'])
        app.sv = sv

    # API
    api.init_app(app)
    app.register_blueprint(apidoc.apidoc)
    return app


def request(verb, url, data, with_token=True):
    '''Make a request to an endpoint.'''
    if with_token:
        data['token'] = get_token()
    return getattr(requests, verb)(url, json=data).json()


def send_notification_messages(messages):
    '''Send notification messages to a Cochicho service.'''
    if messages:
        endpoint = os.path.join(
            current_app.config['COCHICHO_ADDRESS'], 'messages')
        r = request('put', endpoint, {'messages': messages})
        if r.get('status') == 'ok':
            return True
        else:
            raise 'Error sending notifications!'


def scape_template(text):
    return text.replace('$', '$$')
