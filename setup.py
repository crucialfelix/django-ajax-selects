#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(name='bob-ajax-selects',
    version='1.6.1',
    description='jQuery-powered auto-complete fields for editing ForeignKey, ManyToManyField and CharField',
    author='Kamil Warguła, crucialfelix',
    author_email='kwargula@gmail.com crucialfelix@gmail.com',
    url='https://github.com/quamilek/bob-ajax-selects/',
    packages=['ajax_select', ],
    package_data={'ajax_select': ['*.py','*.txt','static/css/*','static/images/*','static/js/*','templates/*.html', 'templates/ajax_select/*.html']},
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Framework :: Django",
        ],
    long_description = """\
Enables editing of `ForeignKey`, `ManyToManyField` and `CharField` using jQuery UI AutoComplete.

1. The user types a search term into the text field
2. An ajax request is sent to the server.
3. The dropdown menu is populated with results.
4. User selects by clicking or using arrow keys
5. Selected result displays in the "deck" area directly below the input field.
6. User can click trashcan icon to remove a selected item

+ Django 1.2+
+ Optional boostrap mode allows easy installation by automatic inclusion of jQueryUI from the googleapis CDN
+ Compatible with staticfiles, appmedia, django-compressor etc
+ Popup to add a new item is supported
+ Admin inlines now supported
+ Ajax Selects works in the admin and also in public facing forms.
+ Rich formatting can be easily defined for the dropdown display and the selected "deck" display.
+ Templates and CSS are fully customizable
+ JQuery triggers enable you to add javascript to respond when items are added or removed, so other interface elements on the page can react
+ Default (but customizable) security prevents griefers from pilfering your data via JSON requests

"""
)
