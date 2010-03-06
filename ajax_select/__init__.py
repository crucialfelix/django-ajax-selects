
from django.conf import settings

from django.forms.models import ModelForm
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.core.exceptions import ImproperlyConfigured

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
    from ajax_select.fields import AutoCompleteField, \
                                   AutoCompleteSelectMultipleField, \
                                   AutoCompleteSelectField

    class TheForm(superclass):
        class Meta:
            pass
        setattr(Meta, 'model', model)

    for model_fieldname,channel in fieldlist.iteritems():

        field = model._meta.get_field(model_fieldname)

        if isinstance(field,ManyToManyField):
            f = AutoCompleteSelectMultipleField(channel,required=not field.blank)
        elif isinstance(field,ForeignKey):
            f = AutoCompleteSelectField(channel,required=not field.blank)
        else:
            f = AutoCompleteField(channel, required=not field.blank)

        # django internals are very difficult to work with.
        # it requires too much knowledge and is thus breakable
        TheForm.declared_fields[model_fieldname] = f
        TheForm.base_fields[model_fieldname] = f
        setattr(TheForm,model_fieldname,f)

    return TheForm




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


