from django.urls import path

from ajax_select import views

urlpatterns = [
    path('ajax_lookup/<channel>',
         views.ajax_lookup,
         name='ajax_lookup')
]
