#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

from ajax_select import fields
# from test_models import Book, Person, Author


class TestAjaxSelectAutoCompleteSelectWidget(unittest.TestCase):

    def setUp(self):
        pass

    def test_render(self):
        channel = None
        widget = fields.AutoCompleteSelectWidget(channel)
        widget

    def tearDown(self):
        pass
