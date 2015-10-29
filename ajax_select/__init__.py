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
from ajax_select.lookup_channel import LookupChannel  # noqa

from .sites import site
from .decorators import register  # noqa


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
