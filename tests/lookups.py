from django.db.models import Q
from django.utils.html import escape
from tests.models import Person
import ajax_select
from ajax_select import LookupChannel


@ajax_select.register('testperson')
class PersonLookup(LookupChannel):

    model = Person

    def get_query(self, q, request):
        return self.model.objects.filter(Q(name__icontains=q) | Q(email__istartswith=q)).order_by('name')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))


class UnregisteredPersonLookup(LookupChannel):

    model = Person

    def get_query(self, q, request):
        return self.model.objects.filter(Q(name__icontains=q) | Q(email__istartswith=q)).order_by('name')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))
