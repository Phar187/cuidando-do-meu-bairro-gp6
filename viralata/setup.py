#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="viralata",
    version='0.2',
    description='Microservice for Authentication: Restlike & Social.',
    author='Andrés M. R. Martano',
    author_email='andres@inventati.org',
    url='https://gitlab.com/cuidandodomeubairro/viralata',
    packages=['viralata'],
    install_requires=[
        'Flask',
        'Flask-Restplus',
        'Flask-CORS',
        'Flask-Mail',
        'Flask-SQLAlchemy',
        # 'python-social-auth',
        'passlib',
        'bleach',
        'sqlalchemy-utils',
        'arrow',
        'psycopg2-binary',  # for Postgres support
    ],
    keywords=['authentication', 'microservice'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Session',
    ]
)
