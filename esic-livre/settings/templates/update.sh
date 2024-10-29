#!/bin/bash

cd $(dirname $BASH_SOURCE)
%(venv_folder)s/bin/flask run_browser >> %(logs_folder)s/update.log
%(venv_folder)s/bin/flask send_notifications >> %(logs_folder)s/update.log
