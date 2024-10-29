# coding: utf-8

import os
from cochicho.app import create_app

settings_folder = os.path.join(os.getcwd(), 'settings')
application = create_app(settings_folder)
