#!/usr/bin/env python
from setuptools import find_packages, setup

from flat_json_widget import get_version

setup(
    name='django-flat-json-widget',
    version=get_version(),
    license='BSD-3-Clause',
    author='OpenWISP',
    author_email='support@openwisp.io',
    description='Django Flat JSON Key/Value Widget',
    long_description=open('README.rst').read(),
    url='https://github.com/openwisp/django-flat-json-widget',
    download_url='https://github.com/openwisp/django-flat-json-widget/releases',
    platforms=['Platform Independent'],
    keywords=['django', 'json', 'key-value', 'widget'],
    packages=find_packages(exclude=['tests*', 'docs*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    extras_require={
        'test': [
            (
                'openwisp-utils[qa]'
                ' @ https://github.com/openwisp/openwisp-utils/tarball/1.2'
            ),
            'django-extensions~=3.2.0',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable ',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
)
