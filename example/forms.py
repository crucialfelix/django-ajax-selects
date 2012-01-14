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
    
    # no help text at all
    label  = make_ajax_field(Release,'label','label',help_text="Search for label by name")
    
    # any extra kwargs are passed onto the field, so you may pass a custom help_text here
    songs = make_ajax_field(Release,'songs','song',help_text=u"Search for song by title")

    # these are from a fixed array defined in lookups.py
    title = make_ajax_field(Release,'title','cliche',help_text=u"Autocomplete will suggest clichés about cats.")

