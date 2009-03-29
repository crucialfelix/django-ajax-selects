
from django.conf import settings
from django.forms.models import ModelForm
from django.db.models.fields.related import ForeignKey, ManyToManyField

def get_lookup(channel):
    """ find the lookup class for the named channel """
    try:
        lookup_label = settings.AJAX_LOOKUP_CHANNELS[channel]
    except (KeyError, AttributeError):
        raise ImproperlyConfigured("settings.AJAX_LOOKUP_CHANNELS not configured correctly for %s" % channel)

    # 'channel' : ('app.module','LookupClass')
    lookup_module = __import__( lookup_label[0],{},{},[''])
    lookup_class = getattr(lookup_module,lookup_label[1] )
    # doesn't have any state so it should really be a singleton
    return lookup_class()



