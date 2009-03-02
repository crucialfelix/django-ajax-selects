
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^ajax_lookup/(?P<channel>[-\w]+)$',
        'ajax_select.views.ajax_lookup',
        name = 'ajax_lookup'
    ),
)

