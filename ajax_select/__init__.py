
from django.conf import settings

def get_lookup(channel):

    try:
        lookup_label = settings.AJAX_LOOKUP_CHANNELS[channel]
    except (KeyError, AttributeError):
        raise ImproperlyConfigured("settings.AJAX_LOOKUP_CHANNELS not configured correctly for %s" % channel)

    # 'channel' : ('app.module','Lookup')
    lookup_module = __import__( lookup_label[0],{},{},[''])
    lookup_class = getattr(lookup_module,lookup_label[1] )
    # doesn't have any state so it should be singleton
    return lookup_class()

