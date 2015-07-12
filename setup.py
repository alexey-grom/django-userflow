#!/usr/bin/env python

from setuptools import setup, find_packages

from userflow import __version__


setup(
    name='userflow',
    version='.'.join(map(str, __version__)),
    description='Another users django app',
    url='https://github.com/alexey-grom/django-userflow',
    author='alxgrmv@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=(
        'django',
        'django-braces',
    ),
)
