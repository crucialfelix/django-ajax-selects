
from ajax_select import get_lookup
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.util import flatatt
from django.template.loader import render_to_string
from django.template.defaultfilters import force_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils import simplejson


as_default_help = u'Enter text to search.'


def _media(self):
    # unless AJAX_SELECT_BOOTSTRAP == False
    # then load jquery and jquery ui + default css
    # where needed
    js = ('ajax_select/js/bootstrap.js', 'ajax_select/js/ajax_select.js')
    try:
        if not settings.AJAX_SELECT_BOOTSTRAP:
            js = ('ajax_select/js/ajax_select.js',)
    except AttributeError:
        pass
    return forms.Media(css={'all': ('ajax_select/css/ajax_select.css',)}, js=js)


####################################################################################


class AutoCompleteSelectWidget(forms.widgets.TextInput):

    """  widget to select a model and return it as text """

    media = property(_media)

    add_link = None

    def __init__(self,
                 channel,
                 help_text=u'',
                 show_help_text=True,
                 plugin_options={},
                 *args,
                 **kwargs):
        self.plugin_options = plugin_options
        super(forms.widgets.TextInput, self).__init__(*args, **kwargs)
        self.channel = channel
        self.help_text = help_text
        self.show_help_text = show_help_text

    def render(self, name, value, attrs=None):

        value = value or ''
        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        current_repr = ''
        initial = None
        lookup = get_lookup(self.channel)
        if value:
            objs = lookup.get_objects([value])
            try:
                obj = objs[0]
            except IndexError:
                raise Exception("%s cannot find object:%s" % (lookup, value))
            current_repr = lookup.format_item_display(obj)
            initial = [current_repr, obj.pk]

        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = u''

        context = {
            'name': name,
            'html_id': self.html_id,
            'current_id': value,
            'current_repr': current_repr,
            'help_text': help_text,
            'extra_attrs': mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-", ""),
            'add_link': self.add_link,
        }
        context.update(plugin_options(lookup, self.channel, self.plugin_options, initial))

        return mark_safe(render_to_string(('autocompleteselect_%s.html' % self.channel, 'autocompleteselect.html'), context))

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
            widget_kwargs = dict(
                channel=channel,
                help_text=kwargs.get('help_text', _(as_default_help)),
                show_help_text=kwargs.pop('show_help_text', True),
                plugin_options=kwargs.pop('plugin_options', {})
            )
            kwargs["widget"] = AutoCompleteSelectWidget(**widget_kwargs)
        super(AutoCompleteSelectField, self).__init__(max_length=255, *args, **kwargs)

    def clean(self, value):
        if value:
            lookup = get_lookup(self.channel)
            objs = lookup.get_objects([value])
            if len(objs) != 1:
                # someone else might have deleted it while you were editing
                # or your channel is faulty
                # out of the scope of this field to do anything more than tell you it doesn't exist
                raise forms.ValidationError(u"%s cannot find object: %s" % (lookup, value))
            return objs[0]
        else:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return None

    def check_can_add(self, user, model):
        _check_can_add(self, user, model)


####################################################################################


class AutoCompleteSelectMultipleWidget(forms.widgets.SelectMultiple):

    """ widget to select multiple models """

    media = property(_media)

    add_link = None

    def __init__(self,
                 channel,
                 help_text='',
                 show_help_text=True,
                 plugin_options={},
                 *args,
                 **kwargs):
        super(AutoCompleteSelectMultipleWidget, self).__init__(*args, **kwargs)
        self.channel = channel

        self.help_text = help_text
        self.show_help_text = show_help_text
        self.plugin_options = plugin_options

    def render(self, name, value, attrs=None):

        if value is None:
            value = []

        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        lookup = get_lookup(self.channel)

        # eg. value = [3002L, 1194L]
        if value:
            # |pk|pk| of current
            current_ids = "|" + "|".join(str(pk) for pk in value) + "|"
        else:
            current_ids = "|"

        objects = lookup.get_objects(value)

        # text repr of currently selected items
        initial = []
        for obj in objects:
            display = lookup.format_item_display(obj)
            initial.append([display, obj.pk])

        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = u''

        context = {
            'name': name,
            'html_id': self.html_id,
            'current': value,
            'current_ids': current_ids,
            'current_reprs': mark_safe(simplejson.dumps(initial)),
            'help_text': help_text,
            'extra_attrs': mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-", ""),
            'add_link': self.add_link,
        }
        context.update(plugin_options(lookup, self.channel, self.plugin_options, initial))

        return mark_safe(render_to_string(('autocompleteselectmultiple_%s.html' % self.channel, 'autocompleteselectmultiple.html'), context))

    def value_from_datadict(self, data, files, name):
        # eg. u'members': [u'|229|4688|190|']
        return [long(val) for val in data.get(name, '').split('|') if val]

    def id_for_label(self, id_):
        return '%s_text' % id_


class AutoCompleteSelectMultipleField(forms.fields.CharField):

    """ form field to select multiple models for a ManyToMany db field """

    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel

        help_text = kwargs.get('help_text')
        show_help_text = kwargs.pop('show_help_text', False)

        if not (help_text is None):
            # '' will cause translation to fail
            # should be u''
            if type(help_text) == str:
                help_text = unicode(help_text)
            # django admin appends "Hold down "Control",..." to the help text
            # regardless of which widget is used. so even when you specify an explicit help text it appends this other default text onto the end.
            # This monkey patches the help text to remove that
            if help_text != u'':
                if type(help_text) != unicode:
                    # ideally this could check request.LANGUAGE_CODE
                    translated = help_text.translate(settings.LANGUAGE_CODE)
                else:
                    translated = help_text
                django_default_help = _(u'Hold down "Control", or "Command" on a Mac, to select more than one.').translate(settings.LANGUAGE_CODE)
                if django_default_help in translated:
                    cleaned_help = translated.replace(django_default_help, '').strip()
                    # probably will not show up in translations
                    if cleaned_help:
                        help_text = cleaned_help
                    else:
                        help_text = u""
                        show_help_text = False
        else:
            help_text = _(as_default_help)

        # django admin will also show help text outside of the display
        # area of the widget.  this results in duplicated help.
        # it should just let the widget do the rendering
        # so by default do not show it in widget
        # if using in a normal form then set to True when creating the field
        widget_kwargs = {
            'channel': channel,
            'help_text': help_text,
            'show_help_text': show_help_text,
            'plugin_options': kwargs.pop('plugin_options', {})
        }
        kwargs['widget'] = AutoCompleteSelectMultipleWidget(**widget_kwargs)
        kwargs['help_text'] = help_text

        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return value  # a list of IDs from widget value_from_datadict

    def check_can_add(self, user, model):
        _check_can_add(self, user, model)


####################################################################################


class AutoCompleteWidget(forms.TextInput):

    """
    Widget to select a search result and enter the result as raw text in the text input field.
    the user may also simply enter text and ignore any auto complete suggestions.
    """

    media = property(_media)

    channel = None
    help_text = ''
    html_id = ''

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        self.help_text = kwargs.pop('help_text', '')
        self.show_help_text = kwargs.pop('show_help_text', True)
        self.plugin_options = kwargs.pop('plugin_options', {})

        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):

        initial = value or ''

        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        lookup = get_lookup(self.channel)
        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = u''

        context = {
            'current_repr': initial,
            'current_id': initial,
            'help_text': help_text,
            'html_id': self.html_id,
            'name': name,
            'extra_attrs': mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-", ""),
        }
        context.update(plugin_options(lookup, self.channel, self.plugin_options, initial))

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

        widget_kwargs = dict(
            help_text=kwargs.get('help_text', _(as_default_help)),
            show_help_text=kwargs.pop('show_help_text', True),
            plugin_options=kwargs.pop('plugin_options', {})
        )
        if 'attrs' in kwargs:
            widget_kwargs['attrs'] = kwargs.pop('attrs')
        widget = AutoCompleteWidget(channel, **widget_kwargs)

        defaults = {'max_length': 255, 'widget': widget}
        defaults.update(kwargs)

        super(AutoCompleteField, self).__init__(*args, **defaults)


####################################################################################

def _check_can_add(self, user, model):
    """ check if the user can add the model, deferring first to
        the channel if it implements can_add()
        else using django's default perm check.
        if it can add, then enable the widget to show the + link
    """
    lookup = get_lookup(self.channel)
    if hasattr(lookup, 'can_add'):
        can_add = lookup.can_add(user, model)
    else:
        ctype = ContentType.objects.get_for_model(model)
        can_add = user.has_perm("%s.add_%s" % (ctype.app_label, ctype.model))
    if can_add:
        self.widget.add_link = reverse('add_popup', kwargs={'app_label': model._meta.app_label, 'model': model._meta.object_name.lower()})


def autoselect_fields_check_can_add(form, model, user):
    """ check the form's fields for any autoselect fields and enable their widgets with + sign add links if permissions allow"""
    for name, form_field in form.declared_fields.iteritems():
        if isinstance(form_field, (AutoCompleteSelectMultipleField, AutoCompleteSelectField)):
            db_field = model._meta.get_field_by_name(name)[0]
            form_field.check_can_add(user, db_field.rel.to)


def plugin_options(channel, channel_name, widget_plugin_options, initial):
    """ Make a JSON dumped dict of all options for the jquery ui plugin itself """
    po = {}
    if initial:
        po['initial'] = initial
    po.update(getattr(channel, 'plugin_options', {}))
    po.update(widget_plugin_options)
    if not po.get('min_length'):
        # backward compatibility: honor the channel's min_length attribute
        # will deprecate that some day and prefer to use plugin_options
        po['min_length'] = getattr(channel, 'min_length', 1)
    if not po.get('source'):
        po['source'] = reverse('ajax_lookup', kwargs={'channel': channel_name})

    # allow html unless explictly false
    if po.get('html') is None:
        po['html'] = True

    return {
        'plugin_options': mark_safe(simplejson.dumps(po)),
        'data_plugin_options': force_escape(simplejson.dumps(po)),
        # continue to support any custom templates that still expect these
        'lookup_url': po['source'],
        'min_length': po['min_length']
        }
