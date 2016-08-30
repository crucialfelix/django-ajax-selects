"""
Test render and submit from the highest Django API level
so we are testing with exactly what Django gives.

Specific errors that are discovered through these tests
should be unit tested in test_fields.py
"""
from __future__ import unicode_literals
from django.forms.models import ModelForm
from django.test import TestCase
from tests.models import Book, Author, Person
from ajax_select import fields
from tests import lookups2  # noqa

# ---------------  setup ----------------------------------- #

class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['name', 'author', 'mentions_persons']

    name = fields.AutoCompleteField('name')
    author = fields.AutoCompleteSelectField('author')
    mentions_persons = fields.AutoCompleteSelectMultipleField('person2')


# ---------------  tests ----------------------------------- #

class TestBookForm(TestCase):

    def test_render_no_data(self):
        form = BookForm()
        out = form.as_p()
        # print(out)
        self.assertTrue('autocomplete' in out)
        self.assertTrue('autocompleteselect' in out)
        self.assertTrue('autocompleteselectmultiple' in out)

    def _make_instance(self):
        author = Author.objects.create(name="author")
        book = Book.objects.create(name="book", author=author)
        book.mentions_persons = [Person.objects.create(name='person')]
        return book

    def _book_data(self, book):
        persons_pks = [person.pk for person in book.mentions_persons.all()]
        mentions_persons = fields.pack_ids(persons_pks)

        return {
            'author': str(book.author.pk),
            'name': book.name,
            'mentions_persons': mentions_persons
        }

    def test_render_instance(self):
        book = self._make_instance()
        form = BookForm(instance=book)
        out = form.as_p()
        # print(out)
        self.assertTrue('autocomplete' in out)
        self.assertTrue('autocompleteselect' in out)
        self.assertTrue('autocompleteselectmultiple' in out)

    def test_render_with_data(self):
        """
        Rendering a form with data already in it
        because it is pre-filled or had errors and is redisplaying.
        """
        book = self._make_instance()
        form = BookForm(data=self._book_data(book))
        out = form.as_p()
        # print(out)
        # should have the values in there somewhere
        self.assertTrue('autocomplete' in out)
        self.assertTrue('autocompleteselect' in out)
        self.assertTrue('autocompleteselectmultiple' in out)

    def test_render_with_initial(self):
        book = self._make_instance()
        # this is data for the form submit
        data = self._book_data(book)
        # initial wants the pks
        data['mentions_persons'] = [p.pk for p in book.mentions_persons.all()]
        form = BookForm(initial=data)
        out = form.as_p()
        # print(out)
        # should have the values in there somewhere
        self.assertTrue('autocomplete' in out)
        self.assertTrue('autocompleteselect' in out)
        self.assertTrue('autocompleteselectmultiple' in out)

    def test_is_valid(self):
        book = self._make_instance()
        form = BookForm(data=self._book_data(book))
        self.assertTrue(form.is_valid())

    def test_full_clean(self):
        book = self._make_instance()
        form = BookForm(data=self._book_data(book))
        form.full_clean()
        data = form.cleaned_data
        # {u'author': <Author: Author object>, u'name': u'book', u'mentions_persons': [u'1']}
        self.assertEqual(data['author'], book.author)
        self.assertEqual(data['name'], book.name)
        # why aren't they instances ?
        self.assertEqual(data['mentions_persons'], [str(p.pk) for p in book.mentions_persons.all()])

    def test_save(self):
        book = self._make_instance()
        form = BookForm(data=self._book_data(book))
        saved = form.save()
        self.assertTrue(saved.pk is not None)

    # def test_save_instance(self):
    #     book = self._make_instance()
    #     form = BookForm(instance=book)
    #     import pdb; pdb.set_trace()
    #     if form.is_valid():
    #         saved = form.save()
    #     else:
    #         print(form.errors)
    #         saved = None
    #     self.assertTrue(saved is not None)
    #     self.assertEqual(saved.pk, book.pk)
