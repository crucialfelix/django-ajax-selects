from django.conf.urls import url

from ajax_select import views

app_name = 'ajax_lookup'

urlpatterns = [
    url(r'^ajax_lookup/(?P<channel>[-\w]+)$',
        views.ajax_lookup,
        name='ajax_lookup')
]
