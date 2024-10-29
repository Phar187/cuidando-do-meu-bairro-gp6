DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@localhost/{database}'

ESIC_EMAIL = "{email}"
ESIC_PASSWORD = "{esic_password}"
FIREFOX_PATH = "/path/to/firefox/binary"
DOWNLOADS_PATH = "/path/where/to/store/ff/downloads"
ATTACHMENT_URL_PREFIX = '{prefix}'
LOG_FOLDER = "/path/to/logs/folder"

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
# The {text} will be set by esiclivre before registering the message.
# The $link will be set by cochicho before sending the message.
NOTIFICATION_TEMPLATE = '''
A Pedido was modified. Check changes!
$link

---

{text}
'''
