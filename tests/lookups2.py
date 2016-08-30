"""
Lookups for the integration tests.
Should load on all django versions,
so it is explicitly imported in test_integration.py
"""
from django.utils.html import escape
from tests.models import Person, Author
import ajax_select


@ajax_select.register('person2')
class PersonsLookup(ajax_select.LookupChannel):

    model = Person

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))

    def format_item_display(self, obj):
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))


@ajax_select.register('name')
class NameLookup(ajax_select.LookupChannel):

    def get_query(self, q, request):
        return ['Joseph Simmons', 'Darryl McDaniels', 'Jam Master Jay']


@ajax_select.register('author')
class AuthorLookup(ajax_select.LookupChannel):

    model = Author
