#!/usr/bin/env python

from distutils.core import setup

setup(name='django-ajax-selects',
    version='1.1.3',
    description='jQuery-powered auto-complete fields for ForeignKey and ManyToMany fields',
    author='crucialfelix',
    author_email='crucialfelix@gmail.com',
    url='http://code.google.com/p/django-ajax-selects/',
    packages=['ajax_select', ],
    include_package_data = True,    # include everything in source control
    package_data={'ajax_select': ['*.py','*.txt','*.css','*.gif','js/*.js','templates/*.html']},
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Framework :: Django",
        ],
    long_description = """\
Enables editing of `ForeignKey`, `ManyToMany` and simple text fields using the Autocomplete - `jQuery` plugin.

django-ajax-selects will work in any normal form as well as in the admin.

The user is presented with a text field.  They type a search term or a few letters of a name they are looking for, an ajax request is sent to the server, a search channel returns possible results.  Results are displayed as a drop down menu.  When an item is selected it is added to a display area just below the text field.

"""
)
