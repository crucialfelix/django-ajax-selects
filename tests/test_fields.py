from django.test import TestCase
from ajax_select import fields


class WidgetTester(TestCase):
    pass


class TestAutoCompleteSelectWidget(WidgetTester):

    def test_render(self):
        channel = 'book'
        widget = fields.AutoCompleteSelectWidget(channel)
        out = widget.render('book', None)
        self.assertTrue('autocompleteselect' in out)


class TestAutoCompleteSelectMultipleWidget(WidgetTester):

    def test_render(self):
        channel = 'book'
        widget = fields.AutoCompleteSelectMultipleWidget(channel)
        out = widget.render('book', None)
        self.assertTrue('autocompleteselectmultiple' in out)


class TestAutoCompleteWidget(WidgetTester):

    def test_render(self):
        channel = 'book'
        widget = fields.AutoCompleteWidget(channel)
        out = widget.render('book', None)
        self.assertTrue('autocomplete' in out)
