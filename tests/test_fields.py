from django.test import TestCase
from ajax_select import fields


class TestAjaxSelectAutoCompleteSelectWidget(TestCase):

    def test_render(self):
        channel = None
        widget = fields.AutoCompleteSelectWidget(channel)
        widget
