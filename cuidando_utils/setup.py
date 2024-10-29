#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="cuidando_utils",
    version='0.1',
    description='Utils for the Cuidando do Meu Bairro Project.',
    author='Andrés M. R. Martano',
    author_email='andres@inventati.org',
    url='https://gitlab.com/cuidandodomeubairro/cuidando_utils',
    packages=["cuidando_utils"],
    install_requires=[
        'Flask',
        'Flask-CORS',
        'Flask-Migrate',
        'Flask-Restplus',
        'Flask-SQLAlchemy',
        'pyjwt',
        'requests',
        'cryptography',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ]
)
