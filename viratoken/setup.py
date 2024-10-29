#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="viratoken",
    version='0.3',
    description='Small lib to encode/decode/sign/verify JWTs '
                'using asymmetric cryptography.',
    author='Andrés M. R. Martano',
    author_email='andres@inventati.org',
    url='https://gitlab.com/cuidandodomeubairro/viratoken',
    packages=["viratoken"],
    install_requires=[
        'cryptography',
        'pyjwt',
    ],
    keywords=['cryptography', 'jwt'],
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
