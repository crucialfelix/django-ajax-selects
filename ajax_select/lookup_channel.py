from django.core.exceptions import PermissionDenied
from django.utils.encoding import force_text
from django.utils.html import escape


class LookupChannel(object):

    """Subclass this, setting model and overiding the methods below to taste"""

    model = None
    plugin_options = {}
    min_length = 1

    def get_query(self, q, request):
        """ return a query set searching for the query string q
            either implement this method yourself or set the search_field
            in the LookupChannel class definition
        """
        kwargs = {"%s__icontains" % self.search_field: q}
        return self.model.objects.filter(**kwargs).order_by(self.search_field)

    def get_result(self, obj):
        """ The text result of autocompleting the entered query """
        return escape(force_text(obj))

    def format_match(self, obj):
        """ (HTML) formatted item for displaying item in the dropdown """
        return escape(force_text(obj))

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return escape(force_text(obj))

    def get_objects(self, ids):
        """ Get the currently selected objects when editing an existing model """
        # return in the same order as passed in here
        # this will be however the related objects Manager returns them
        # which is not guaranteed to be the same order they were in when you last edited
        # see OrdredManyToMany.md
        pk_type = self.model._meta.pk.to_python
        ids = [pk_type(id) for id in ids]
        things = self.model.objects.in_bulk(ids)
        return [things[aid] for aid in ids if aid in things]

    def can_add(self, user, argmodel):
        """ Check if the user has permission to add
            one of these models. This enables the green popup +
            Default is the standard django permission check
        """
        from django.contrib.contenttypes.models import ContentType
        ctype = ContentType.objects.get_for_model(argmodel)
        return user.has_perm("%s.add_%s" % (ctype.app_label, ctype.model))

    def check_auth(self, request):
        """ to ensure that nobody can get your data via json simply by knowing the URL.
            public facing forms should write a custom LookupChannel to implement as you wish.
            also you could choose to return HttpResponseForbidden("who are you?")
            instead of raising PermissionDenied (401 response)
         """
        if not request.user.is_staff:
            raise PermissionDenied
