
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from ajax_select import get_lookup


class AutoCompleteSelectWidget(forms.widgets.TextInput):
    """  widget to select a model """

    html_id = ''

    def __init__(self,
                 channel,
                 help_text='',
                 *args, **kw):
        super(forms.widgets.TextInput, self).__init__(*args, **kw)
        # url for Datasource
        self.channel = channel
        self.help_text = help_text

    def render(self, name, value, attrs=None):
        if value == None:
            value = ''
        html_id = attrs.get('id', name)
        self.html_id = html_id

        lookup = get_lookup(self.channel)
        if value:
            current_name = lookup.get_objects([value])[0]
        else:
            current_name = ''
        lookup_url = reverse('ajax_lookup',kwargs={'channel':self.channel})
        vars = dict(name=name, html_id=html_id,lookup_url=lookup_url,current_id=value,current_name=current_name,help_text=self.help_text)
        return mark_safe(render_to_string(('autocompleteselect_%s.html' % self.channel, 'autocompleteselect.html'),vars))

    def value_from_datadict(self, data, files, name):

        got = data.get(name, None)
        if got:
            return long(got)
        else:
            return None



class AutoCompleteSelectField(forms.fields.CharField):
    """  form field to select a model for a ForeignKey db field """
    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        super(AutoCompleteSelectField, self).__init__(
            widget = AutoCompleteSelectWidget(channel=channel,help_text=kwargs.get('help_text','')),
            max_length=255,
            *args, **kwargs)

    def clean(self, value):
        return value # id of object
        # possible error condition if someone else deleted object while you editing





class AutoCompleteSelectMultipleWidget(forms.widgets.SelectMultiple):

    """ widget to select multiple models """

    html_id = ''
    
    def __init__(self,
                 channel,
                 help_text='',
                 *args, **kw):
        super(AutoCompleteSelectMultipleWidget, self).__init__(*args, **kw)
        self.channel = channel
        self.help_text = help_text

    def render(self, name, value, attrs=None):
        if value == None:
            value = []
        html_id = attrs.get('id', name)
        self.html_id = html_id

        lookup = get_lookup(self.channel)
        lookup_url = reverse('ajax_lookup',kwargs={'channel':self.channel})

        current_name = ""# the text field starts empty
        # value = [3002L, 1194L]
        if value:
            current_ids = "|" + "|".join( str(id) for id in value ) + "|" # id|id of current
        else:
            current_ids = "|"
        
        objects = lookup.get_objects(value)
        
        # text repr of currently selected items
        current_repr = []
        current_repr_json = []
        for obj in objects:
            repr = lookup.format_item(obj)
            current_repr_json.append( """new Array("%s",%s)""" % (repr,obj.id) )

        current_reprs = mark_safe("new Array(%s)" % ",".join(current_repr_json))
        
        vars = dict(name=name,
         html_id=html_id,
         lookup_url=lookup_url,
         current=value,
         current_name=current_name,
         current_ids=current_ids,
         current_reprs=current_reprs,
         help_text=self.help_text
         )
        return mark_safe(render_to_string(('autocompleteselectmultiple_%s.html' % self.channel, 'autocompleteselectmultiple.html'),vars))



    def value_from_datadict(self, data, files, name):
        #eg u'members': [u'|229|4688|190|']
        return [long(val) for val in data.get(name,'').split('|') if val]




class AutoCompleteSelectMultipleField(forms.fields.CharField):
    """ form field to select multiple models for a ManyToMany db field """

    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        kwargs['widget'] = AutoCompleteSelectMultipleWidget(channel=channel,help_text=kwargs.get('help_text',''))
        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value # a list of IDs from widget value_from_datadict
        # should: check that none of the objects have been deleted by somebody else


