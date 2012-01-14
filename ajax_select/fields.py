
from ajax_select import get_lookup
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.util import flatatt
from django.template.defaultfilters import escapejs
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
import os



####################################################################################

class AutoCompleteSelectWidget(forms.widgets.TextInput):

    """  widget to select a model and return it as text """

    add_link = None

    def __init__(self,
                 channel,
                 help_text='',
                 show_help_text=False,
                 *args, **kw):
        super(forms.widgets.TextInput, self).__init__(*args, **kw)
        self.channel = channel
        self.help_text = help_text
        self.show_help_text = show_help_text

    def render(self, name, value, attrs=None):

        value = value or ''
        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        lookup = get_lookup(self.channel)
        if value:
            objs = lookup.get_objects([value])
            try:
                obj = objs[0]
            except IndexError:
                raise Exception("%s cannot find object:%s" % (lookup, value))
            display = lookup.format_item_display(obj)
            current_repr = mark_safe( """new Array("%s",%s)""" % (escapejs(display),obj.pk) )
        else:
            current_repr = 'null'

        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = ''

        context = {
                'name': name,
                'html_id' : self.html_id,
                'min_length': getattr(lookup, 'min_length', 1),
                'lookup_url': reverse('ajax_lookup',kwargs={'channel':self.channel}),
                'current_id': value,
                'current_repr': current_repr,
                'help_text': help_text,
                'extra_attrs': mark_safe(flatatt(final_attrs)),
                'func_slug': self.html_id.replace("-",""),
                'add_link' : self.add_link,
                }
        context.update(bootstrap())
        
        return mark_safe(render_to_string(('autocompleteselect_%s.html' % self.channel, 'autocompleteselect.html'),context))

    def value_from_datadict(self, data, files, name):

        got = data.get(name, None)
        if got:
            return long(got)
        else:
            return None

    def id_for_label(self, id_):
        return '%s_text' % id_



class AutoCompleteSelectField(forms.fields.CharField):

    """  form field to select a model for a ForeignKey db field """

    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        widget = kwargs.get("widget", False)
        
        if not widget or not isinstance(widget, AutoCompleteSelectWidget):
            help_text = kwargs.get('help_text',_('Enter text to search.'))
            show_help_text = kwargs.pop('show_help_text',False)
            kwargs["widget"] = AutoCompleteSelectWidget(channel=channel,help_text=help_text,show_help_text=show_help_text)
        super(AutoCompleteSelectField, self).__init__(max_length=255,*args, **kwargs)

    def clean(self, value):
        if value:
            lookup = get_lookup(self.channel)
            objs = lookup.get_objects( [ value] )
            if len(objs) != 1:
                # someone else might have deleted it while you were editing
                # or your channel is faulty
                # out of the scope of this field to do anything more than tell you it doesn't exist
                raise forms.ValidationError(u"%s cannot find object: %s" % (lookup,value))
            return objs[0]
        else:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return None

    def check_can_add(self,user,model):
        _check_can_add(self,user,model)


####################################################################################


class AutoCompleteSelectMultipleWidget(forms.widgets.SelectMultiple):

    """ widget to select multiple models """

    add_link = None

    def __init__(self,
                 channel,
                 help_text='',
                 show_help_text=False,
                 *args, **kwargs):
        super(AutoCompleteSelectMultipleWidget, self).__init__(*args, **kwargs)
        self.channel = channel
        
        self.help_text = help_text or _('Enter text to search.')
        self.show_help_text = show_help_text

    def render(self, name, value, attrs=None):

        if value is None:
            value = []

        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        lookup = get_lookup(self.channel)

        # eg. value = [3002L, 1194L]
        if value:
            current_ids = "|" + "|".join( str(pk) for pk in value ) + "|" # |pk|pk| of current
        else:
            current_ids = "|"

        objects = lookup.get_objects(value)

        # text repr of currently selected items
        current_repr_json = []
        for obj in objects:
            display = lookup.format_item_display(obj)
            current_repr_json.append( """new Array("%s",%s)""" % (escapejs(display),obj.pk) )
        current_reprs = mark_safe("new Array(%s)" % ",".join(current_repr_json))
        
        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = ''
        
        context = {
            'name':name,
            'html_id':self.html_id,
            'min_length': getattr(lookup, 'min_length', 1),
            'lookup_url':reverse('ajax_lookup',kwargs={'channel':self.channel}),
            'current':value,
            'current_ids':current_ids,
            'current_reprs': current_reprs,
            'help_text':help_text,
            'extra_attrs': mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-",""),
            'add_link' : self.add_link,
        }
        context.update(bootstrap())

        return mark_safe(render_to_string(('autocompleteselectmultiple_%s.html' % self.channel, 'autocompleteselectmultiple.html'),context))

    def value_from_datadict(self, data, files, name):
        # eg. u'members': [u'|229|4688|190|']
        return [long(val) for val in data.get(name,'').split('|') if val]

    def id_for_label(self, id_):
        return '%s_text' % id_



class AutoCompleteSelectMultipleField(forms.fields.CharField):

    """ form field to select multiple models for a ManyToMany db field """

    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel

        as_default_help = u'Enter text to search.'
        help_text = kwargs.get('help_text')
        if not (help_text is None):
            try:
                en_help = help_text.translate('en')
            except AttributeError:
                pass
            else:
                # monkey patch the django default help text to the ajax selects default help text
                django_default_help = u'Hold down "Control", or "Command" on a Mac, to select more than one.'
                if django_default_help in en_help:
                    en_help = en_help.replace(django_default_help,'').strip()
                    # probably will not show up in translations
                    if en_help:
                        help_text = _(en_help)
                    else:
                        help_text = _(as_default_help)
        else:
            help_text = _(as_default_help)

        # admin will also show help text, so by default do not show it in widget
        # if using in a normal form then set to True so the widget shows help
        show_help_text = kwargs.pop('show_help_text',False)
        
        kwargs['widget'] = AutoCompleteSelectMultipleWidget(channel=channel,help_text=help_text,show_help_text=show_help_text)
        kwargs['help_text'] = help_text
        
        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return value # a list of IDs from widget value_from_datadict

    def check_can_add(self,user,model):
        _check_can_add(self,user,model)


####################################################################################


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
        self.show_help_text = kwargs.pop('show_help_text',False)
        
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):

        value = value or ''
        
        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        lookup = get_lookup(self.channel)
        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = ''
        context = {
            'current_repr': value,
            'current_id': value,
            'help_text': help_text,
            'html_id': self.html_id,
            'min_length': getattr(lookup, 'min_length', 1),
            'lookup_url': reverse('ajax_lookup', args=[self.channel]),
            'name': name,
            'extra_attrs':mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-",""),
        }
        context.update(bootstrap())

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

        widget_kwargs = dict(help_text=kwargs.get('help_text', _('Enter text to search.')))
        widget_kwargs['show_help_text'] = kwargs.pop('show_help_text',False)
        if 'attrs' in kwargs:
            widget_kwargs['attrs'] = kwargs.pop('attrs')
        widget = AutoCompleteWidget(channel,**widget_kwargs)

        defaults = {'max_length': 255,'widget': widget}
        defaults.update(kwargs)

        super(AutoCompleteField, self).__init__(*args, **defaults)


####################################################################################

def _check_can_add(self,user,model):
    """ check if the user can add the model, deferring first to 
        the channel if it implements can_add()
        else using django's default perm check.
        if it can add, then enable the widget to show the + link 
    """
    lookup = get_lookup(self.channel)
    if hasattr(lookup,'can_add'):
        can_add = lookup.can_add(user,model)
    else:
        ctype = ContentType.objects.get_for_model(model)
        can_add = user.has_perm("%s.add_%s" % (ctype.app_label,ctype.model))
    if can_add:
        self.widget.add_link = reverse('add_popup',
            kwargs={'app_label':model._meta.app_label,'model':model._meta.object_name.lower()})


def autoselect_fields_check_can_add(form,model,user):
    """ check the form's fields for any autoselect fields and enable their widgets with + sign add links if permissions allow"""
    for name,form_field in form.declared_fields.iteritems():
        if isinstance(form_field,(AutoCompleteSelectMultipleField,AutoCompleteSelectField)):
            db_field = model._meta.get_field_by_name(name)[0]
            form_field.check_can_add(user,db_field.rel.to)


def bootstrap():
    b = {}
    b['bootstrap'] = getattr(settings,'AJAX_SELECT_BOOTSTRAP',False)
    inlines = getattr(settings,'AJAX_SELECT_INLINES',None)

    b['inline'] = ''
    if inlines == 'inline':
        directory = os.path.dirname( os.path.realpath(__file__) )
        f = open(os.path.join(directory,"static","css","ajax_select.css"))
        css = f.read()
        f = open(os.path.join(directory,"static","js","ajax_select.js"))
        js = f.read()
        b['inline'] = mark_safe(u"""<style type="text/css">%s</style><script type="text/javascript">//<![CDATA[%s//]]></script>""" % (css,js))
    elif inlines == 'staticfiles':
        b['inline'] = mark_safe("""<style type="text/css">@import url("%sajax_select/css/ajax_select.css");</style><script type="text/javascript" src="%sajax_select/js/ajax_select.js"></script>""" % (settings.STATIC_URL,settings.STATIC_URL))

    return b


