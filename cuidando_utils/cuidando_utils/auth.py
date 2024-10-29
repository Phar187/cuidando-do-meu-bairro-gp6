import requests
from flask import current_app


def register():
    '''Create a user in a Viralata instance.'''
    config = current_app.config
    r = requests.post(
        config['VIRALATA_ADDRESS'] + '/users',
        json={
            'username': config['VIRALATA_USER'],
            'password': config['VIRALATA_PASSWORD'],
            'email': config['VIRALATA_EMAIL']
        })
    response = r.json()
    if 'message' in response:
        print(response['message'])


def get_token(type_='micro'):
    '''Get a token from a Viralata instance.'''
    config = current_app.config
    r = requests.post(
        config['VIRALATA_ADDRESS'] + '/login/local',
        json={
            'username': config['VIRALATA_USER'],
            'password': config['VIRALATA_PASSWORD']
        })
    tokens = r.json()
    return tokens[f'{type_}Token']
