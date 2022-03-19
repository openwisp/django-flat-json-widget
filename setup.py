#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

from flat_json_widget import get_version

if sys.argv[-1] == 'publish':
    # delete any *.pyc, *.pyo and __pycache__
    os.system('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload -s dist/*')
    os.system('rm -rf dist build')
    args = {'version': get_version()}
    print('You probably want to also tag the version now:')
    print('  git tag -a %(version)s -m "version %(version)s"' % args)
    print('  git push --tags')
    sys.exit()


setup(
    name='django-flat-json-widget',
    version=get_version(),
    license='BSD-3-Clause',
    author='Federico Capoano',
    author_email='federico.capoano@gmail.com',
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
            'openwisp-utils[qa]~=1.0.0',
            'django-extensions~=3.1.0',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
)
