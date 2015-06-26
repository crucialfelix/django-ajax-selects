from django.db.models import Q
from django.utils.html import escape

import ajax_select
from ajax_select import LookupChannel

from .test_models import Person

from django.test import TestCase

@ajax_select.register('testperson')
class PersonLookup(LookupChannel):
    model = Person

    def get_query(self, q, request):
        return Person.objects.filter(Q(name__icontains=q) | Q(email__istartswith=q)).order_by('name')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return u"%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))


class UnregisteredPersonLookup(LookupChannel):
    model = Person

    def get_query(self, q, request):
        return Person.objects.filter(Q(name__icontains=q) | Q(email__istartswith=q)).order_by('name')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return u"%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))

class TestPersonLookup(TestCase):
    def setUp(self):
        pass

    def test_person_lookup_is_registered(self):
        self.assertIsNotNone(ajax_select.site._registry.get('testperson'))

    def test_unregistered_person_lookup_is_not_registered(self):
        self.assertIsNone(ajax_select.site._registry.get('testunregisteredperson'))