#!/bin/bash

cd $(dirname $BASH_SOURCE)
%(venv_folder)s/bin/flask update_data >> %(logs_folder)s/update.log
%(venv_folder)s/bin/flask send_notifications >> %(logs_folder)s/update.log
