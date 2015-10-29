"""Testing if lookups that are not in a file named lookups.py can be loaded correctly."""

import ajax_select
from tests.models import Book


class BookLookup(ajax_select.LookupChannel):

    model = Book
