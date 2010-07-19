"""JQuery-Ajax Autocomplete fields for Django Forms"""
__version__ = "1.1.4"
__author__ = "crucialfelix"
__contact__ = "crucialfelix@gmail.com"
__homepage__ = "http://code.google.com/p/django-ajax-selects/"

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.models import ModelForm
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _, ugettext


def make_ajax_form(model,fieldlist,superclass=ModelForm):
    """ this will create a ModelForm subclass inserting
            AutoCompleteSelectMultipleField (many to many),
            AutoCompleteSelectField (foreign key)

        where specified in the fieldlist:

            dict(fieldname='channel',...)

        usage:
            class YourModelAdmin(Admin):
                ...
                form = make_ajax_form(YourModel,dict(contacts='contact',author='contact'))

            where 'contacts' is a many to many field, specifying to use the lookup channel 'contact'
            and
            where 'author' is a foreign key field, specifying here to also use the lookup channel 'contact'

    """

    class TheForm(superclass):
        class Meta:
            pass
        setattr(Meta, 'model', model)

    for model_fieldname,channel in fieldlist.iteritems():
        f = make_ajax_field(model,model_fieldname,channel)
        
        TheForm.declared_fields[model_fieldname] = f
        TheForm.base_fields[model_fieldname] = f
        setattr(TheForm,model_fieldname,f)

    return TheForm


def make_ajax_field(model,model_fieldname,channel,**kwargs):
    """ makes an ajax select / multiple select / autocomplete field
        copying the label and help text from the model's db field
    
        optional args:
            help_text - note that django's ManyToMany db field will append 
                'Hold down "Control", or "Command" on a Mac, to select more than one.'
                to your db field's help text.
                Therefore you are better off passing it in here
            label - default is db field's verbose name
            required - default's to db field's (not) blank
            """

    from ajax_select.fields import AutoCompleteField, \
                                   AutoCompleteSelectMultipleField, \
                                   AutoCompleteSelectField

    field = model._meta.get_field(model_fieldname)
    if kwargs.has_key('label'):
        label = kwargs.pop('label')
    else:
        label = _(capfirst(unicode(field.verbose_name)))
    if kwargs.has_key('help_text'):
        help_text = kwargs.pop('help_text')
    else:
        if isinstance(field.help_text,basestring):
            help_text = _(field.help_text)
        else:
            help_text = field.help_text
    if kwargs.has_key('required'):
        required = kwargs.pop('required')
    else:
        required = not field.blank

    if isinstance(field,ManyToManyField):
        f = AutoCompleteSelectMultipleField(
            channel,
            required=required,
            help_text=help_text,
            label=label,
            **kwargs
            )
    elif isinstance(field,ForeignKey):
        f = AutoCompleteSelectField(
            channel,
            required=required,
            help_text=help_text,
            label=label,
            **kwargs
            )
    else:
        f = AutoCompleteField(
            channel,
            required=required,
            help_text=help_text,
            label=label,
            **kwargs
            )
    return f

def get_lookup(channel):
    """ find the lookup class for the named channel.  this is used internally """
    try:
        lookup_label = settings.AJAX_LOOKUP_CHANNELS[channel]
    except (KeyError, AttributeError):
        raise ImproperlyConfigured("settings.AJAX_LOOKUP_CHANNELS not configured correctly for %r" % channel)

    if isinstance(lookup_label,dict):
        # 'channel' : dict(model='app.model', search_field='title' )
        # generate a simple channel dynamically
        return make_channel( lookup_label['model'], lookup_label['search_field'] )
    else:
        # 'channel' : ('app.module','LookupClass')
        # from app.module load LookupClass and instantiate
        lookup_module = __import__( lookup_label[0],{},{},[''])
        lookup_class = getattr(lookup_module,lookup_label[1] )
        return lookup_class()


def make_channel(app_model,search_field):
    """ used in get_lookup
        app_model :   app_name.model_name
        search_field :  the field to search against and to display in search results """
    from django.db import models
    app_label, model_name = app_model.split(".")
    model = models.get_model(app_label, model_name)

    class AjaxChannel(object):

        def get_query(self,q,request):
            """ return a query set searching for the query string q """
            kwargs = { "%s__icontains" % search_field : q }
            return model.objects.filter(**kwargs).order_by(search_field)

        def format_item(self,obj):
            """ format item for simple list of currently selected items """
            return unicode(obj)

        def format_result(self,obj):
            """ format search result for the drop down of search results. may include html """
            return unicode(obj)

        def get_objects(self,ids):
            """ get the currently selected objects """
            return model.objects.filter(pk__in=ids).order_by(search_field)

    return AjaxChannel()


