#!/usr/bin/env python
# coding: utf-8

import sys

import flask
from flask import g, url_for

from social.apps.flask_app.default.models import init_social
from social.actions import do_auth, do_complete
from social.apps.flask_app.utils import load_strategy, load_backend
from social.backends.facebook import FacebookOAuth2
from social.strategies.flask_strategy import FlaskStrategy
from social.utils import build_absolute_uri
# from social.strategies.utils import set_current_strategy_getter
# from social.apps.flask_app.routes import social_auth
# from social.apps.flask_app.template_filters import backends

from cuidando_utils import db


def init_social_models(app):
    try:
        import viralata
    except:
        sys.path.append('..')
    init_social(app, db.session)


# set_current_strategy_getter(load_strategy)


def get_auth_url(backend, redirect_uri, *args, **kwargs):
    uri = redirect_uri
    if uri and not uri.startswith('/'):
        uri = url_for(uri, backend=backend)

    g.strategy = load_strategy()
    g.backend = load_backend(g.strategy, backend, redirect_uri=uri,
                             *args, **kwargs)
    resp = do_auth(g.backend)
    return resp.location


def get_username(backend, redirect_uri):
    g.strategy = load_strategy()
    g.backend = load_backend(g.strategy, backend, redirect_uri=redirect_uri)
    do_complete(g.backend, login=do_login)
    return g.user.username


class HeadlessFacebookStrategy(FlaskStrategy):
    name = 'facebook'

    def build_absolute_uri(self, path=None):
        # TODO: Quando a API diretamente (e não a partir de outro site) não tem
        # "referrer". Como resolver isso?
        return build_absolute_uri(
            flask.request.referrer, path).partition("&")[0]


class HeadlessFacebookBackend(FacebookOAuth2):
    name = 'facebook'

    def validate_state(self):
        if not self.STATE_PARAMETER and not self.REDIRECT_STATE:
            return None
        # state = self.get_session_state()
        request_state = self.get_request_state()
        # if not request_state:
        #     raise AuthMissingParameter(self, 'state')
        return request_state

    def request(self, url, method='GET', *args, **kwargs):
        from social.utils import user_agent
        from social.exceptions import AuthFailed
        from requests import request as req
        kwargs.setdefault('headers', {})
        if self.setting('VERIFY_SSL') is not None:
            kwargs.setdefault('verify', self.setting('VERIFY_SSL'))
        kwargs.setdefault('timeout', self.setting('REQUESTS_TIMEOUT') or
                          self.setting('URLOPEN_TIMEOUT'))

        if self.SEND_USER_AGENT and 'User-Agent' not in kwargs['headers']:
            kwargs['headers']['User-Agent'] = user_agent()

        try:
            # import IPython; IPython.embed()
            response = req(method, url, *args, **kwargs)
        except ConnectionError as err:
            raise AuthFailed(self, str(err))
        try:
            response.raise_for_status()
        except:
            print(response.json())
            print(url)
            print(kwargs)
            raise
        return response


def do_login(backend, user, social_user):
    print("do_login", user, social_user)


def insert_user(user, is_new, **kwargs):
    '''This function is used to add the user to the global var that will be used
    get_username'''
    if user:
        g.user = user
