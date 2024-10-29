bind = 'unix:%(code_folder)s/gunicorn.sock'
workers = 3
accesslog = '%(logs_folder)s/access.log'
errorlog = '%(logs_folder)s/error.log'
loglevel = 'debug'
proc_name = '%(service)s'
