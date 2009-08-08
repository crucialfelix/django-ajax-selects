
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from ajax_select import get_lookup
from django.forms.util import flatatt



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
        html_id = attrs.get('pk', name)
        self.html_id = html_id

        lookup = get_lookup(self.channel)
        if value:
            current_name = lookup.get_objects([value])[0]
        else:
            current_name = ''
        lookup_url = reverse('ajax_lookup',kwargs={'channel':self.channel})
        vars = dict(
                name=name,
                html_id=html_id,
                lookup_url=lookup_url,
                current_id=value,
                current_name=current_name,
                help_text=self.help_text,
                extra_attrs=mark_safe(flatatt(self.attrs))
                )        
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
        widget = kwargs.get("widget", False)
        if not widget or not isinstance(widget, AutoCompleteSelectWidget):
            kwargs["widget"] = AutoCompleteSelectWidget(channel=channel,help_text=kwargs.get('help_text',''))

        super(AutoCompleteSelectField, self).__init__(
            max_length=255,
            *args, **kwargs)

    def clean(self, value):
        if value:
            lookup = get_lookup(self.channel)
            objs = lookup.get_objects( [ value] )
            if len(objs) != 1:
                # someone else might have deleted it while you were editing
                # or your channel is faulty
                # out of the scope of this app to do anything more than tell you it doesn't exist
                raise forms.ValidationError(u"The selected item does not exist.")
            return objs[0]
        else:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return None





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
        html_id = attrs.get('pk', name)
        self.html_id = html_id

        lookup = get_lookup(self.channel)
        lookup_url = reverse('ajax_lookup',kwargs={'channel':self.channel})

        current_name = ""# the text field starts empty
        # value = [3002L, 1194L]
        if value:
            current_ids = "|" + "|".join( str(pk) for pk in value ) + "|" # pk|pk of current
        else:
            current_ids = "|"

        objects = lookup.get_objects(value)

        # text repr of currently selected items
        current_repr = []
        current_repr_json = []
        for obj in objects:
            repr = lookup.format_item(obj)
            current_repr_json.append( """new Array("%s",%s)""" % (repr,obj.pk) )

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
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return value # a list of IDs from widget value_from_datadict
        # should: check that none of the objects have been deleted by somebody else while we were editing


class AutoCompleteWidget(forms.TextInput):
    """
    Widget to select a search result and enter the result as raw text in the text input field.
    the user may also simply enter text and ignore any auto complete suggestions.
    """
    channel = None
    help_text = ''
    html_id = ''

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        self.help_text = kwargs.pop('help_text', '')

        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if attrs is not None:
            html_id = attrs.get('pk', name)
        else:
            html_id = name

        self.html_id = html_id
        value = value or ''

        context = {
            'current_name': value,
            'current_id': value,
            'help_text': self.help_text,
            'html_id': self.html_id,
            'lookup_url': reverse('ajax_lookup', args=[self.channel]),
            'name': name,
        }

        templates = ('autocomplete_%s.html' % self.channel,
                     'autocomplete.html')
        return mark_safe(render_to_string(templates, context))


class AutoCompleteField(forms.CharField):
    """
    Field uses an AutoCompleteWidget to lookup possible completions using a channel and stores raw text (not a foreign key)
    """
    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel

        widget = AutoCompleteWidget(channel,
                                    help_text=kwargs.get('help_text', ''))

        defaults = {'max_length': 255,
                    'widget': widget}
        defaults.update(kwargs)

        super(AutoCompleteField, self).__init__(*args, **defaults)

