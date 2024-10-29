#!/usr/bin/env python
# coding: utf-8

import re

import bleach
import passlib
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
# from flask import redirect, url_for, make_response
from flask_restplus import Resource
from flask_mail import Message
from flask import current_app

from cuidando_utils import db, sv, ExtraApi

# from viralata.auths import get_auth_url, get_username
from viralata.models import User


class ViralataApi(ExtraApi):

    # Replace API method
    def decode_token(self, token):
        decoded = self.decode_validate_token(token)

        # Verify if main token is not invalid
        if decoded['type'] == 'main':
            user = get_user(decoded['username'])
            if decoded['exp'] != user.last_token_exp:
                self.abort_with_msg(400, 'Invalid main token!', ['token'])

        return decoded


api = ViralataApi(version='1.0',
                  title='Vira-lata',
                  description='An authentication microservice.')

api.update_parser_arguments({
    'username': {
        'location': 'json',
        'help': 'The username.',
    },
    'password': {
        'location': 'json',
        'help': 'The password.',
    },
    'new_password': {
        'location': 'json',
        'help': 'A new password, when changing the current one.',
    },
    'code': {
        'location': 'json',
        'help': 'A temporary code used to reset the password.',
    },
    'email': {
        'location': 'json',
        'help': 'The email.',
    },
    'description': {
        'location': 'json',
        'help': 'The user description.',
    },
    'users': {
        'location': 'json',
        'type': list,
        'help': 'A list of usernames.',
    },
})


# @api.route('/login/external/manual/<string:backend>')
# class LoginExtManAPI(Resource):

#     def get(self, backend):
#         '''Asks the URL that should be used to login with a specific backend
#         (like Facebook).'''
#         return {'redirect': get_auth_url(backend, 'loginextmanapi')}


# @api.route('/complete/manual/<string:backend>')
# class CompleteLoginExtManAPI(Resource):

#     def post(self, backend):
#         '''Completes the login with a specific backend.'''
#         username = get_username(backend, redirect_uri='/')
#         return create_tokens(username)


# @api.route('/login/external/automatic/<string:backend>')
# class StartLoginExtAutoAPI(Resource):

#     def get(self, backend):
#         '''Asks the URL that should be used to login with a specific backend
#         (like Facebook).'''
#         print('AUTH-GET')
#         print(get_auth_url(backend, 'completeloginautoapi'))
#         return {'redirect': get_auth_url(backend, 'completeloginautoapi')}
#         # return redirect(get_auth_url(backend, 'completeloginautoapi'))

# @api.route('/complete/automatic/<string:backend>')
# class CompleteLoginAutoAPI(Resource):

#     def get(self, backend):
#         '''Completes the login with a specific backend.'''
#         print('COMPLETE-GET')
#         username = get_username(backend,
#                                 url_for('completeloginautoapi',
#                                         backend='facebook'))
#         tokens = create_tokens(username)
#         response = redirect("http://localhost:5001/")
#         # import IPython; IPython.embed()
#         return response
#         # return create_tokens(username)


@api.route('/login/local')
class LoginLocalAPI(Resource):

    @api.parsed_args('username', 'password')
    def post(self, username, password):
        '''Login using local DB, not a third-party service.'''
        try:
            if User.verify_user_password(username, password):
                return create_tokens(username)
            else:
                api.abort_with_msg(400, 'Wrong password...', ['password'])
        except NoResultFound:
            api.abort_with_msg(400,
                               'Username seems not registered...',
                               ['username'])


@api.route('/renew_micro_token')
class RenewMicroToken(Resource):

    # TODO: oq fazer nesse caso?
    @api.parsed_args('token', parse_token=False)
    def post(self, token):
        '''Get a new micro token to be used with the other microservices.'''
        decoded = self.decode_token(token)
        if decoded['type'] != 'main':
            # This seems not to be a main token. It must be main for security
            # reasons, for only main ones can be invalidated at logout.
            # Allowing micro tokens would allow infinite renew by a
            # compromised token
            api.abort_with_msg(400, 'Must use a main token', ['token'])

        token = create_token(decoded['username']),
        return {
            'microToken': token,
            'microTokenValidPeriod': current_app.config[
                'MICRO_TOKEN_VALID_PERIOD'],
        }


@api.route('/reset_password')
class ResetPassword(Resource):

    @api.parsed_args('username', 'email')
    def post(self, username, email):
        '''Sends an email to the user with a code to reset password.'''
        user = get_user(username)

        check_user_email(user, email)

        msg = Message(
            current_app.config['MAIL_SUBJECT'],
            sender=current_app.config['SENDER_NAME'],
            recipients=[user.email])

        code = passlib.utils.generate_password(15)
        exp = current_app.config['TIME_RESET_PASSWORD']
        user.set_temp_password(code, exp)
        db.session.commit()
        msg.body = (current_app.config['EMAIL_TEMPLATE']
                    .format(code=code, exp_min=exp/60))
        api.mail.send(msg)
        return {
            'message': 'Check email!',
            'exp': exp,
        }

    @api.parsed_args('username', 'email', 'code', 'password')
    def put(self, username, email, code, password):
        '''Change the password of a user using a temporary code.'''
        validate_password(password)
        user = get_user(username)
        check_user_email(user, email)
        if not user.check_temp_password(code):
            api.abort_with_msg(400, 'Invalid code', ['code'])
        user.hash_password(password)
        # Commit is done by create_tokens
        return create_tokens(username)


@api.route('/logout')
class Logout(Resource):

    @api.parsed_args('token')
    def post(self, username):
        '''Invalidates the main token.'''
        args = api.general_parse()
        decoded = self.decode_token(args['token'])
        # Invalidates all main tokens
        get_user(decoded['username']).last_token_exp = 0
        db.session.commit()
        return {}


@api.route('/users/<string:username>')
class UserAPI(Resource):

    @api.parsed_args('optional_token')
    def get(self, token_username, username):
        '''Get information about an user.'''
        try:
            user = User.get_user(username)
        except NoResultFound:
            api.abort_with_msg(404, 'User not found', ['username'])

        resp = {
            'username': user.username,
            'description': user.description,
        }

        # Add email if this is the owner of the account
        if token_username == username:
            resp['email'] = user.email
        return resp

    @api.parsed_args('token', 'description', 'email', 'password', 'new_password')
    def put(self, token_username, username, description=None, email=None,
            password=None, new_password=None):
        '''Edit information about an user.'''
        if username == token_username:
            user = get_user(token_username)
            changed = False

            # If is changing password
            if password:
                if user.verify_password(password):
                    validate_password(new_password, 'new_password')
                    user.hash_password(new_password)
                    changed = True
                else:
                    api.abort_with_msg(400, 'Wrong password...', ['password'])

            # If is changing description
            if description:
                user.description = bleach.clean(description, strip=True)
                changed = True

            # If is changing email
            if email:
                validate_email(email)
                user.email = email
                changed = True

            # If some data seems to have changed, commit
            if changed:
                db.session.commit()

            return {
                'username': user.username,
                'description': user.description,
                'email': user.email,
            }

        else:
            api.abort_with_msg(550, 'Editing other user profile...',
                               ['username', 'token'])


@api.route('/users')
class UsersAPI(Resource):

    @api.parsed_args('token', 'users')
    def get(self, username, users=[]):
        '''Get data about users. Must be a special user.'''
        users = db.session.query(User).filter(User.username.in_(users)).all()
        if username and username in current_app.config['SPECIAL_USERS']:
            return {
                'users': {u.username: {'email': u.email} for u in users}
            }
        else:
            api.abort_with_msg(400, 'User not found', ['username'])
        # else:
        #     return {
        #         'users': [u.username for u in users]
        #     }

    @api.parsed_args('username', 'password', 'email')
    def post(self, username, password, email):
        '''Register a new user.'''
        # TODO: case insensitive? ver isso na hora de login tb
        # username = username.lower()
        if len(username) < 5 or len(username) > 40:
            api.abort_with_msg(
                400,
                'Invalid username size. Must be between 5 and 40 characters.',
                ['username'])
        if not re.match(r'[A-Za-z0-9]{5,}', username):
            api.abort_with_msg(400, 'Invalid characters in username...',
                               ['username'])

        validate_password(password)
        validate_email(email)

        user = User(username=username, email=email)
        user.hash_password(password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            api.abort_with_msg(
                400,
                'Error to create user.'
                ' Maybe username is already registered...',
                ['username'])
        return create_tokens(username)


@api.route('/users_list')
class ListUsersAPI(Resource):

    @api.parsed_args()
    def get(self):
        '''Get usernames.'''
        usernames = db.session.query(User.username).all()
        return {
            'users': [u[0] for u in usernames]
        }


# def create_token(username, exp_minutes=5):
#     '''Returns a token.'''
#     return sv.encode({
#         'username': username,
#     }, exp_minutes)


def create_tokens(username):
    '''Returns new main and micro tokens for the user.'''
    main_token = create_token(username, True)
    user = get_user(username)
    # TODO: Talvez usar algo mais rápido para decodificar o token,
    # como ignorar verificações?
    user.last_token_exp = sv.decode(main_token)['exp']
    db.session.commit()
    return {
        'mainToken': main_token,
        'microToken': create_token(username),
        'microTokenValidPeriod': current_app.config['MICRO_TOKEN_VALID_PERIOD'],
        'mainTokenValidPeriod': current_app.config['MAIN_TOKEN_VALID_PERIOD'],
    }


def create_token(username, main=False):
    '''Returns a token for the passed username.
    "main" controls the type of the token.'''

    if main:
        exp_minutes = current_app.config['MAIN_TOKEN_VALID_PERIOD']
        token_type = 'main'
    else:
        exp_minutes = current_app.config['MICRO_TOKEN_VALID_PERIOD']
        token_type = 'micro'

    return sv.encode({
        'username': username,
        'type': token_type,
    }, exp_minutes)


def get_user(username):
    try:
        return User.get_user(username)
    except NoResultFound:
        # Returning 400 because 404 adds another msg that corrupts the json
        api.abort_with_msg(400, 'User not found', ['username'])


def validate_password(password, fieldname='password'):
    '''Check if is a valid password. The fieldname parameter is used to
    specify the fieldname in the error message.'''
    if len(password) < 5:
        api.abort_with_msg(
            400,
            'Invalid password. Needs at least 5 characters.',
            [fieldname])
    if not re.match(r'[A-Za-z0-9@#$%^&+=]{5,}', password):
        api.abort_with_msg(
            400,
            'Invalid characters in password...',
            [fieldname])


def validate_email(email):
    '''Check if is a valid email.'''
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        api.abort_with_msg(400, 'Invalid email', ['email'])


def check_user_email(user, email):
    if user.email != email:
        api.abort_with_msg(400, 'Wrong email.', ['email'])
