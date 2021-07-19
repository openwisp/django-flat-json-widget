django-flat-json-widget
=======================

.. image:: https://github.com/openwisp/django-flat-json-widget/workflows/Django%20Flat%20JSON%20Widget%20CI%20Build/badge.svg?branch=master
   :target: https://github.com/openwisp/openwisp-controller/actions?query=workflow%3A%22Django%20Flat%20JSON%20Widget%20CI%20Build%22
   :alt: CI build status

.. image:: https://coveralls.io/repos/openwisp/django-flat-json-widget/badge.svg
  :target: https://coveralls.io/r/openwisp/django-flat-json-widget
   :alt: Test Coverage

.. image:: https://requires.io/github/openwisp/django-flat-json-widget/requirements.svg?branch=master
   :target: https://requires.io/github/openwisp/django-flat-json-widget/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://img.shields.io/gitter/room/nwjs/nw.js.svg
   :target: https://gitter.im/openwisp/general
   :alt: Chat

.. image:: https://badge.fury.io/py/django-flat-json-widget.svg
   :target: http://badge.fury.io/py/django-flat-json-widget
   :alt: Pypi Version

.. image:: https://pepy.tech/badge/django-flat-json-widget
   :target: https://pepy.tech/project/django-flat-json-widget
   :alt: Downloads

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://pypi.org/project/black/
   :alt: code style: black

.. image:: https://raw.githubusercontent.com/openwisp/django-flat-json-widget/master/docs/django-flat-json-widget-demo.gif
  :target: https://github.com/openwisp/django-flat-json-widget/tree/master/docs/django-flat-json-widget-demo.gif
  :alt: Django Flat JSON (key/value) Widget

------------

If you ever needed to store a flexible dictionary of keys and values in your
django models, you may have felt the need of giving your users a widget to
easily manipulate the data by adding or removing rows,
instead of having to edit the raw JSON.

This package solves exactly that problem: **it offers a widget to manipulate
a flat JSON object made of simple keys and values**.

Compatibility
-------------

Tested on python >= 3.7 and Django >= 3.0.

It should work also on previous versions of Django.

Install stable version from pypi
--------------------------------

Install from pypi:

.. code-block:: shell

    pip install django-flat-json-widget

Usage
-----

Add ``flat_json_widget`` to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # other apps...
        'flat_json_widget',
    ]

Then load the widget where you need it, for example, here's how to use it in the
django admin site:

.. code-block:: python

    from django.contrib import admin
    from django import forms
    from .models import JsonDocument

    from flat_json_widget.widgets import FlatJsonWidget


    class JsonDocumentForm(forms.ModelForm):
        class Meta:
            widgets = {
                'content': FlatJsonWidget
            }


    @admin.register(JsonDocument)
    class JsonDocumentAdmin(admin.ModelAdmin):
        list_display = ['name']
        form = JsonDocumentForm

Installing for development
--------------------------

Install your forked repo:

.. code-block:: shell

    git clone git://github.com/<your_fork>/django-flat-json-widget
    cd django-flat-json-widget/
    python setup.py develop

Install development dependencies:

.. code-block:: shell

    pip install -e .[test]
    npm install -g jslint stylelint

Create database:

.. code-block:: shell

    cd tests/
    ./manage.py migrate
    ./manage.py createsuperuser

Launch development server:

.. code-block:: shell

    ./manage.py runserver 0.0.0.0:8000

You can access the admin interface at http://127.0.0.1:8000/admin/.

Run tests with:

.. code-block:: shell

    ./runtests.py

Run quality assurance tests with:

.. code-block:: shell

    ./run-qa-checks

Contributing
------------

Please refer to the `OpenWISP contributing guidelines <http://openwisp.io/docs/developer/contributing.html>`_.

Changelog
---------

See `CHANGES <https://github.com/openwisp/django-flat-json-widget/blob/master/CHANGES.rst>`_.

License
-------

See `LICENSE <https://github.com/openwisp/django-flat-json-widget/blob/master/LICENSE>`_.

Support
-------

See `OpenWISP Support Channels <http://openwisp.org/support.html>`_.
