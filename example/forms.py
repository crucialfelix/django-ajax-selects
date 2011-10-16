# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import ModelForm
from ajax_select import make_ajax_field
from example.models import Release


class ReleaseForm(ModelForm):

    class Meta:
        model = Release

    #           args:  this model, fieldname on this model, lookup_channel_name
    group  = make_ajax_field(Release,'group','group')
    label  = make_ajax_field(Release,'label','label')
    
    # any extra kwargs are passed onto the field, so you may pass a custom help_text here
    songs = make_ajax_field(Release,'songs','song',help_text=u"Search for song by title")

    # if you are creating a form for use outside of the django admin to specify show_m2m_help=True :
    # label  = make_ajax_field(Release,'label','label',show_m2m_help=True)
    # so that it will show the help text in manytomany fields 

    title = make_ajax_field(Release,'title','cliche',help_text=u"Autocomplete will search the database for clichés about cats.")

