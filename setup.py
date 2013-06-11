#!/usr/bin/env python

import os
from setuptools import setup

__author__ = 'Akretion : aymeric.lecomte@akretion.com sebastien.beau@akretion.com'
__version__ = '0.1.0'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    # Basic package information.
    name = 'mondialrelay_pyt',
    version = __version__,

    # Packaging options.
    include_package_data = True,

    # Package dependencies.
#    install_requires = ['lxml'] 

    # Metadata for PyPI.
    author = 'Aymeric Lecomte, Sebastien Beau',
    author_email = 'aymeric.lecomte@akretion.com, sebastien.beau@akretion.com',
    license = 'GNU AGPL-3',
    url = 'http://github.com/akretion/mondialrelay_pyt',
    packages=['mondialrelay_pyt'],
    keywords = 'mondial relay api client',
    description = 'A library to access Mondial Relay WSI2_CreateEtiquette Web Service from Python.',
    long_description = read('README.md'),
    classifiers = [
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet'
    ]
)
