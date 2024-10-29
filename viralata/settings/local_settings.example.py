DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@localhost/{database}'
SOCIAL_AUTH_FACEBOOK_KEY = '{your_facebook_dev_key}'
SOCIAL_AUTH_FACEBOOK_SECRET = '{your_facebook_dev_secret}'

# This is required for PSA for sessions, even though we are not using them...
SECRET_KEY = '{long_string...}'

# Password to unlock key. Use None if no password is needed.
PRIVATE_KEY_PASSWORD = '{your_key_password}'

# Users allowed to get email addresses from other users
SPECIAL_USERS = ['{username}']


# ----------------------------- #
# Forgot password functionality #
# ----------------------------- #

__username__ = '{email_username}'

# These are used to send e-mails to the admin when a comment is reported.
MAIL_SERVER = '{email_server_address}'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = __username__
MAIL_PASSWORD = '{email_password}'
SENDER_NAME = __username__

MAIL_SUBJECT = 'New password request'
