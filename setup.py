#!/usr/bin/env python3

from setuptools import setup

setup(
    name='cophi-toolbox',
    version='0.0.1dev1',
    description='Cophi toolbox',
    author=", ".join(['Thorsten Vitt <thorsten.vitt@uni-wuerzburg.de>',
                      'Fotis Jannidis <fotis.jannidis@uni-wuerzburg.de>']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    packages=['ctoolbox'],
    setup_requires=[
        'numpy'       # work around https://github.com/numpy/numpy/issues/2434
    ],
    install_requires=[
        'matplotlib>=1.3.1',
        'numpy>=1.8.1',
        'pandas>=0.13.1',
        'scipy>=0.14.0',
        'regex'
    ],
    test_suite='nose.collector'
)
