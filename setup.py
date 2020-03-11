#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

DOC_NAME = 'README.md'

import os
from setuptools import setup, find_packages

long_description = """
"""

if os.path.isfile(DOC_NAME):
    with open(DOC_NAME, encoding='utf-8') as fp:
        long_description = fp.read()

long_description = long_description or ''

setup(
    long_description=long_description,
    packages=find_packages(),
    # auto generated:
    name='theconf',
    version='0.1.3',
    description='',
    keywords=['singleton', 'configuration', 'config', 'yaml', 'ArgumentParser', 'mlflow', 'torch'],
    author='clint',
    author_email='clint.b@kakaobrain.com',
    url='https://github.com/wbaek/theconf',
    classifiers=[],
    scripts=[],
    entry_points={},
    zip_safe=False,
    include_package_data=True,
    setup_requires=[],
    install_requires=[
        'pyyaml',
        'GitPython',
        'mlflow',
        'torch',
        'tensorboard'
    ],
    tests_require=[],
)
