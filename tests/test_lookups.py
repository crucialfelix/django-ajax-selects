
# conflicting models
# import sys; print(sys.path)
# from .models import Person

from django.test import TestCase
import ajax_select
from .lookups import PersonLookup, UnregisteredPersonLookup  # noqa


class TestPersonLookup(TestCase):

    def test_person_lookup_is_registered(self):
        self.assertIsNotNone(ajax_select.site._registry.get('testperson'))

    def test_unregistered_person_lookup_is_not_registered(self):
        self.assertIsNone(ajax_select.site._registry.get('testunregisteredperson'))
