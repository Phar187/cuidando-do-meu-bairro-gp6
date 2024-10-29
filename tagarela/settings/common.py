SQLALCHEMY_TRACK_MODIFICATIONS = False

# Max age for tokens used to delete reported comments
MAX_AGE_REPORT_TOKENS = 7 * 24 * 60 * 60

# This is the content of the e-mail sent for the admins when
# someone reports a comment.
EMAIL_TEMPLATE = '''
Someone reported a comment as abusive.
To delete it open this link:
{delete_link}

Comment:
ID: {id}
Author: {author}
Created: {created}
Modified: {modified}
Thread: {thread}
Text: {text}
'''
