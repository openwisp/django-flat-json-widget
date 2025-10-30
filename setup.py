#!/usr/bin/env python
from setuptools import find_packages, setup

from flat_json_widget import get_version

setup(
    name="django-flat-json-widget",
    version=get_version(),
    license="BSD-3-Clause",
    author="OpenWISP",
    author_email="support@openwisp.io",
    description="Django Flat JSON Key/Value Widget",
    long_description=open("README.rst").read(),
    url="https://github.com/openwisp/django-flat-json-widget",
    download_url="https://github.com/openwisp/django-flat-json-widget/releases",
    platforms=["Platform Independent"],
    keywords=["django", "json", "key-value", "widget"],
    packages=find_packages(exclude=["tests*", "docs*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "django>=4.2,<5.3",
    ],
    extras_require={
        "test": [
            (
                "openwisp-utils[qa,selenium] @"
                " https://github.com/openwisp/openwisp-utils/archive/"
                "refs/heads/1.3.tar.gz"
            ),
            "django-extensions>=3.2,<4.2",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
