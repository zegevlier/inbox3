#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

settings.update(
    name='inbox3',
    version='0.0.1',
    description='SMTP Server for Humans with asyncio.',
    long_description=open('README.rst').read(),
    author='Minchul Lee',
    author_email='2_minchul@naver.com',
    url='https://github.com/2minchul/inbox3',
    py_modules=['inbox3', ],
    install_requires=['logbook', 'argparse', 'aiosmtpd'],
    license='BSD',
    classifiers=(
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    )
)

setup(**settings)
