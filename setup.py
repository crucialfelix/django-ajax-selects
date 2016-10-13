#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='django-ajax-selects',
    version='1.5.1',
    description='Edit ForeignKey, ManyToManyField and CharField in Django Admin using jQuery UI AutoComplete.',
    author='Chris Sattinger',
    author_email='crucialfelix@gmail.com',
    url='https://github.com/crucialfelix/django-ajax-selects/',
    packages=['ajax_select'],
    package_data={'ajax_select':
        [
            '*.py',
            '*.txt',
            '*.md',
            'static/ajax_select/css/*',
            'static/ajax_select/images/*',
            'static/ajax_select/js/*',
            'templates/ajax_select/*.html'
        ]
    },
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Framework :: Django",
    ],
    long_description="""\
Edit ForeignKey, ManyToManyField and CharField in Django Admin using jQuery UI AutoComplete.

- Customize search query
- Query other resources besides Django ORM
- Format results with HTML
- Customize styling
- Customize security policy
- Add additional custom UI alongside widget
- Integrate with other UI elements elsewhere on the page using the javascript API
- Works in Admin as well as in normal views

- Django >=1.6, <=1.10
- Python >=2.7, <=3.5
"""
)
