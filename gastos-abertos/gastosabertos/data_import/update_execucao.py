#!/usr/bin/env python
# coding: utf-8

'''Downloads the execucao data for the current year, checks if the file
changed and updates the DB if so.

Usage:
    ./update_execucao [options]

Options:
    -h --help                                 Show this message.
    -r --remove                               Remove CSV and older history after import.
    -i --instance <instance_folder_path>      Instance folder path.
    -s --store-folder <store_folder_path>     Folder where to store downloaded.
    -p --public-folder <public_folder_path>   Folder where to store files to be
                                              downloaded.
'''

from __future__ import unicode_literals  # unicode by default
import os
import shutil
import filecmp
from datetime import date, timedelta

from docopt import docopt

# from utils import get_db
from .import_execucao import update_from_csv, remove_older_history
from .update_execucao_year_info import update_all_years_info
from .geocode_execucao import geocode_all
from .generate_execucao_csv import generate_year
from .execucao_downloader import download_year, convert_to_csv
# from import_execucao import insert_csv
# ga_dados_path = os.path.join(*['/'] +
#                              os.getcwd().split('/')[1:-2] +
#                              ['gastos_abertos_dados'])


def update(db, storing_folder, public_downloads, remove_old=False):
    current_year = str(date.today().year)
    tmp_folder = os.path.join('/', 'tmp')

    filepath = download_year(current_year, tmp_folder)

    last_file = os.path.join(storing_folder, 'last.ods')
    if os.path.exists(last_file) and filecmp.cmp(filepath, last_file):
        print('File seems the same, nothing to do...')
        os.remove(filepath)
    else:
        print('File changed! Updating...')
        csvfilepath = convert_to_csv(filepath, tmp_folder)
        newfilepath = os.path.join(storing_folder,
                                   '{0}.{1}'.format(str(date.today()), 'csv'))
        shutil.move(csvfilepath, newfilepath)
        update_from_csv(db, newfilepath)
        if remove_old:
            os.remove(newfilepath)
            remove_older_history(db, timedelta(weeks=4))

        print('Geocoding...')
        geocode_all(db)
        update_all_years_info(db)
        shutil.move(filepath, last_file)
        print('Generating CSV...')
        generate_year(db, current_year, public_downloads)
        print('Done.')


if __name__ == '__main__':
    from utils import get_db
    db = get_db()
    arguments = docopt(__doc__)

    # # ga_dados_path = os.path.join('..', '..', 'gastos_abertos_dados')
    # ga_dados_path = arguments['--ga-dados']
    # # public_downloads = os.path.join('..', '..', 'public-downloads', 'execucao')
    public_downloads = arguments['--public-folder']
    # # sys.path.append(ga_dados_path)

    # # storing_folder = os.path.join(ga_dados_path, 'Orcamento', 'execucao', 'diario')
    storing_folder = arguments['--store-folder']

    update(db, storing_folder, public_downloads, arguments['--remove'])
