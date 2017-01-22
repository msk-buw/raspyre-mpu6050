#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A setuptools based setup module for Raspyre"""

from codecs import open
from os import path
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'raspyre',
    'smbus2'
]

test_requirements = [
    'raspyre',
    'pytest'
]

setup(
    name='raspyre-mpu6050',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="MPU6050 sensor driver for the raspyre framework",
    long_description=readme + '\n\n' + history,
    author="Jan Frederick Eick",
    author_email='jan-frederick.eick@uni-weimar.de',
    url='',
    ackages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
    #    'console_scripts':[
    #        'raspyre=raspyre.cli:cli',
    #        ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
