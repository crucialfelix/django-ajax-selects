from django.test import TestCase
from ajax_select import fields
from tests.models import Book


class TestAutoCompleteSelectWidget(TestCase):

    def test_render(self):
        channel = 'book'
        widget = fields.AutoCompleteSelectWidget(channel)
        out = widget.render('book', None)
        self.assertTrue('autocompleteselect' in out)

    def test_render_with_value(self):
        channel = 'book'
        widget = fields.AutoCompleteSelectWidget(channel)
        book = Book.objects.create(name='book')
        out = widget.render('book', book.pk)
        self.assertTrue('autocompleteselect' in out)


class TestAutoCompleteSelectMultipleWidget(TestCase):

    def test_render(self):
        channel = 'book'
        widget = fields.AutoCompleteSelectMultipleWidget(channel)
        out = widget.render('book', None)
        self.assertTrue('autocompleteselectmultiple' in out)

    def test_render_with_query_set(self):
        channel = 'book'
        widget = fields.AutoCompleteSelectMultipleWidget(channel)
        Book.objects.create(name='book')
        out = widget.render('book', Book.objects.all())
        self.assertTrue('autocompleteselectmultiple' in out)


class TestAutoCompleteWidget(TestCase):

    def test_render(self):
        channel = 'book'
        widget = fields.AutoCompleteWidget(channel)
        out = widget.render('book', None)
        self.assertTrue('autocomplete' in out)


class TestAutoCompleteSelectField(TestCase):

    def test_has_changed(self):
        field = fields.AutoCompleteSelectField('book')
        self.assertFalse(field.has_changed(1, '1'))
        self.assertFalse(field.has_changed('abc', 'abc'))
        self.assertTrue(field.has_changed(1, '2'))
        self.assertFalse(field.has_changed(None, ''))
        self.assertFalse(field.has_changed(None, None))
        self.assertFalse(field.has_changed('', None))


class TestAutoCompleteSelectMultipleField(TestCase):

    def test_has_changed(self):
        field = fields.AutoCompleteSelectMultipleField('book')
        self.assertFalse(field.has_changed([1], ['1']))
        self.assertFalse(field.has_changed(['abc'], ['abc']))
        self.assertTrue(field.has_changed([1], ['2']))

    def test_has_changed_blank_input(self):
        field = fields.AutoCompleteSelectMultipleField('book')
        self.assertTrue(field.has_changed(None, ['1']))
        self.assertFalse(field.has_changed(None, []))
