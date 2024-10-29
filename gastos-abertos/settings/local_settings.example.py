DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@localhost/{database}'

STORAGE_FOLDER = '/path/store/downloaded/files'
PUBLIC_DOWNLOADS_FOLDER = '/path/store/files/public/can/download'

# -------- #
# Viralata #
# -------- #
VIRALATA_ADDRESS = 'https://{viralata_address}:{viralata_port}'
VIRALATA_USER = '{esiclivre_viralata_username}'
VIRALATA_PASSWORD = '{user_password}'
VIRALATA_EMAIL = '{user_email}'

# -------- #
# Cochicho #
# -------- #
COCHICHO_ADDRESS = 'https://{cochicho_address}:{cochicho_port}'
NOTIFICATION_TITLE = '{notification_email_title}'
# Notification message template
# The {description} and {changes} will be set by gastosabertos before registering the message.
# The $link will be set by cochicho before sending the message.
NOTIFICATION_TEMPLATE = '''
A expense was modified. Check changes!
$link
---
{description}
---
Changes:
{changes}
'''
