# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='gastosabertos',
    version='0.2',
    url='https://gitlab.com/cuidandodomeubairro/gastos-abertos',
    description='Sao Paulo city public spending data.',
    author='Andrés M. R. Martano',
    author_email='andres@inventati.org',
    packages=['gastosabertos'],
    # include_package_data=True,
    # zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Restplus',
        'Flask-CORS',
        'geoalchemy2',
        'docopt',
        'pandas',
        'geopy',
        'shapely',
        'psycopg2-binary',
        'xlrd',
        'pyexcel',
        'pyexcel-xls',
        'pyexcel-ods3',
        'lxml',
        'ezodf',
        # 'futures',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ]
)
