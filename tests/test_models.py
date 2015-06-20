#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-ajax-selects
------------

Tests for `django-ajax-selects` models module.
"""

# import unittest
from django.db import models


# ---------------------------  models ---------------------------------- #

class Person(models.Model):

    name = models.CharField()

    class Meta:
        app_label = 'testapp'

class Author(models.Model):

    name = models.CharField()

    class Meta:
        app_label = 'testapp'


class Book(models.Model):

    """ Book has no admin, its an inline in the Author admin"""

    author = models.ForeignKey(Author)
    name = models.CharField()
    mentions_persons = models.ManyToManyField(Person, help_text="MENTIONS PERSONS HELP TEXT")

    class Meta:
        app_label = 'testapp'
# ---------------------------  tests ---------------------------------- #

# class TestAjax_select(unittest.TestCase):

#     def setUp(self):
#         pass

#     def test_something(self):
#         pass

#     def tearDown(self):
#         pass
