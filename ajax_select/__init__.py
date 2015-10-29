"""JQuery-Ajax Autocomplete fields for Django Forms"""
__version__ = "1.3.6"
__author__ = "crucialfelix"
__contact__ = "crucialfelix@gmail.com"
__homepage__ = "https://github.com/crucialfelix/django-ajax-selects/"

from django import VERSION
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.models import ModelForm
from django.utils.text import capfirst
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from ajax_select.helpers import make_ajax_form, make_ajax_field  # noqa

from .sites import site
from .decorators import register  # noqa


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



# -----------------------   private  --------------------------------------------- #

def get_lookup(channel):
    """ find the lookup class for the named channel.  this is used internally """
    try:
        lookup_label = site._registry[channel]
    except KeyError:
        raise ImproperlyConfigured("settings.AJAX_LOOKUP_CHANNELS not configured correctly for %(channel)r "
                                   "or autodiscovery could not locate %(channel)r" % {'channel': channel})

    if isinstance(lookup_label, dict):
        # 'channel' : dict(model='app.model', search_field='title' )
        #  generate a simple channel dynamically
        return make_channel(lookup_label['model'], lookup_label['search_field'])
    else:  # a tuple
        # 'channel' : ('app.module','LookupClass')
        #  from app.module load LookupClass and instantiate
        lookup_module = __import__(lookup_label[0], {}, {}, [''])
        lookup_class = getattr(lookup_module, lookup_label[1])

        # monkeypatch older lookup classes till 1.3
        if not hasattr(lookup_class, 'format_match'):
            setattr(lookup_class, 'format_match',
                getattr(lookup_class, 'format_item',
                    lambda self, obj: force_text(obj)))
        if not hasattr(lookup_class, 'format_item_display'):
            setattr(lookup_class, 'format_item_display',
                getattr(lookup_class, 'format_item',
                    lambda self, obj: force_text(obj)))
        if not hasattr(lookup_class, 'get_result'):
            setattr(lookup_class, 'get_result',
                getattr(lookup_class, 'format_result',
                    lambda self, obj: force_text(obj)))

        return lookup_class()


def make_channel(app_model, arg_search_field):
    """ used in get_lookup
            app_model :   app_name.model_name
            search_field :  the field to search against and to display in search results
    """
    from django.db import models
    app_label, model_name = app_model.split(".")
    themodel = models.get_model(app_label, model_name)

    class MadeLookupChannel(LookupChannel):

        model = themodel
        search_field = arg_search_field

    return MadeLookupChannel()


def autodiscover():
    try:
        from django.utils.module_loading import autodiscover_modules
    except ImportError:
        raise ImproperlyConfigured("AJAX_LOOKUP_CHANNELS is not set in settings.py and we cannot do "
                                   "app autodiscovery unless Django version is >=1.7")
    autodiscover_modules('lookups', register_to=site)


if VERSION[:2] <= (1, 6):
    # Django <= 1.6, use settings.AJAX_LOOKUP_CHANNELS only
    try:
        site.register(settings.AJAX_LOOKUP_CHANNELS)
    except AttributeError:
        pass  # Allow AJAX_LOOKUP_CHANNELS to be empty and fail at the point of get_lookup()
else:
    default_app_config = 'ajax_select.apps.AjaxSelectConfig'
