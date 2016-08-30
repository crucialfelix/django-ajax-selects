from __future__ import unicode_literals
import json
from ajax_select.registry import registry
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
try:
    from django.forms.utils import flatatt
except ImportError:
    # < django 1.7
    from django.forms.util import flatatt
from django.template.loader import render_to_string
from django.template.defaultfilters import force_escape
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.six import text_type
from django.utils.translation import ugettext as _


as_default_help = 'Enter text to search.'


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

    """Widget to search for a model and return it as text for use in a CharField."""

    media = property(_media)

    add_link = None

    def __init__(self,
                 channel,
                 help_text='',
                 show_help_text=True,
                 plugin_options=None,
                 *args,
                 **kwargs):
        self.plugin_options = plugin_options or {}
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
        lookup = registry.get(self.channel)
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
            help_text = ''

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
        context.update(make_plugin_options(lookup, self.channel, self.plugin_options, initial))
        templates = (
            'ajax_select/autocompleteselect_%s.html' % self.channel,
            'ajax_select/autocompleteselect.html')
        out = render_to_string(templates, context)
        return mark_safe(out)

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)

    def id_for_label(self, id_):
        return '%s_text' % id_


class AutoCompleteSelectField(forms.fields.CharField):

    """Form field to select a Model for a ForeignKey db field."""

    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel

        widget_kwargs = dict(
            channel=channel,
            help_text=kwargs.get('help_text', _(as_default_help)),
            show_help_text=kwargs.pop('show_help_text', True),
            plugin_options=kwargs.pop('plugin_options', {})
        )
        widget_kwargs.update(kwargs.pop('widget_options', {}))
        kwargs["widget"] = AutoCompleteSelectWidget(**widget_kwargs)
        super(AutoCompleteSelectField, self).__init__(max_length=255, *args, **kwargs)

    def clean(self, value):
        if value:
            lookup = registry.get(self.channel)
            objs = lookup.get_objects([value])
            if len(objs) != 1:
                # someone else might have deleted it while you were editing
                # or your channel is faulty
                # out of the scope of this field to do anything more than tell you it doesn't exist
                raise forms.ValidationError("%s cannot find object: %s" % (lookup, value))
            return objs[0]
        else:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return None

    def check_can_add(self, user, model):
        _check_can_add(self, user, model)

    def has_changed(self, initial, data):
        # 1 vs u'1'
        initial_value = initial if initial is not None else ''
        data_value = data if data is not None else ''
        return text_type(initial_value) != text_type(data_value)


####################################################################################


class AutoCompleteSelectMultipleWidget(forms.widgets.SelectMultiple):

    """Widget to select multiple models for a ManyToMany db field."""

    media = property(_media)

    add_link = None

    def __init__(self,
                 channel,
                 help_text='',
                 show_help_text=True,
                 plugin_options=None,
                 *args,
                 **kwargs):
        super(AutoCompleteSelectMultipleWidget, self).__init__(*args, **kwargs)
        self.channel = channel

        self.help_text = help_text
        self.show_help_text = show_help_text
        self.plugin_options = plugin_options or {}

    def render(self, name, value, attrs=None):

        if value is None:
            value = []

        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        lookup = registry.get(self.channel)

        if isinstance(value, QuerySet):
            objects = value
        else:
            objects = lookup.get_objects(value)

        current_ids = pack_ids([obj.pk for obj in objects])

        # text repr of currently selected items
        initial = [
            [lookup.format_item_display(obj), obj.pk]
            for obj in objects
        ]

        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = ''

        context = {
            'name': name,
            'html_id': self.html_id,
            'current': value,
            'current_ids': current_ids,
            'current_reprs': mark_safe(json.dumps(initial)),
            'help_text': help_text,
            'extra_attrs': mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-", ""),
            'add_link': self.add_link,
        }
        context.update(make_plugin_options(lookup, self.channel, self.plugin_options, initial))
        templates = ('ajax_select/autocompleteselectmultiple_%s.html' % self.channel,
                    'ajax_select/autocompleteselectmultiple.html')
        out = render_to_string(templates, context)
        return mark_safe(out)

    def value_from_datadict(self, data, files, name):
        # eg. 'members': ['|229|4688|190|']
        return [val for val in data.get(name, '').split('|') if val]

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
            # should be ''
            if isinstance(help_text, str):
                help_text = force_text(help_text)
            # django admin appends "Hold down "Control",..." to the help text
            # regardless of which widget is used. so even when you specify an explicit
            # help text it appends this other default text onto the end.
            # This monkey patches the help text to remove that
            if help_text != '':
                if not isinstance(help_text, text_type):
                    # ideally this could check request.LANGUAGE_CODE
                    translated = help_text.translate(settings.LANGUAGE_CODE)
                else:
                    translated = help_text
                dh = 'Hold down "Control", or "Command" on a Mac, to select more than one.'
                django_default_help = _(dh).translate(settings.LANGUAGE_CODE)
                if django_default_help in translated:
                    cleaned_help = translated.replace(django_default_help, '').strip()
                    # probably will not show up in translations
                    if cleaned_help:
                        help_text = cleaned_help
                    else:
                        help_text = ""
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
        widget_kwargs.update(kwargs.pop('widget_options', {}))
        kwargs['widget'] = AutoCompleteSelectMultipleWidget(**widget_kwargs)
        kwargs['help_text'] = help_text

        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return value  # a list of primary keys from widget value_from_datadict

    def check_can_add(self, user, model):
        _check_can_add(self, user, model)

    def has_changed(self, initial_value, data_value):
        # [1, 2] vs [u'1', u'2']
        ivs = [text_type(v) for v in (initial_value or [])]
        dvs = [text_type(v) for v in (data_value or [])]
        return ivs != dvs

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

        lookup = registry.get(self.channel)
        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = ''

        context = {
            'current_repr': initial,
            'current_id': initial,
            'help_text': help_text,
            'html_id': self.html_id,
            'name': name,
            'extra_attrs': mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-", ""),
        }
        context.update(make_plugin_options(lookup, self.channel, self.plugin_options, initial))
        templates = ('ajax_select/autocomplete_%s.html' % self.channel,
                     'ajax_select/autocomplete.html')
        return mark_safe(render_to_string(templates, context))


class AutoCompleteField(forms.CharField):
    """
    A CharField that uses an AutoCompleteWidget to lookup matching and stores the result as plain text.
    """
    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel

        widget_kwargs = dict(
            help_text=kwargs.get('help_text', _(as_default_help)),
            show_help_text=kwargs.pop('show_help_text', True),
            plugin_options=kwargs.pop('plugin_options', {})
        )
        widget_kwargs.update(kwargs.pop('widget_options', {}))
        if 'attrs' in kwargs:
            widget_kwargs['attrs'] = kwargs.pop('attrs')
        widget = AutoCompleteWidget(channel, **widget_kwargs)

        defaults = {'max_length': 255, 'widget': widget}
        defaults.update(kwargs)

        super(AutoCompleteField, self).__init__(*args, **defaults)


####################################################################################

def _check_can_add(self, user, related_model):
    """
    Check if the User can create a related_model.

    If the LookupChannel implements check_can_add() then use this.

    Else uses Django's default permission system.

    If it can add, then enable the widget to show the green + link
    """
    lookup = registry.get(self.channel)
    if hasattr(lookup, 'can_add'):
        can_add = lookup.can_add(user, related_model)
    else:
        ctype = ContentType.objects.get_for_model(related_model)
        can_add = user.has_perm("%s.add_%s" % (ctype.app_label, ctype.model))
    if can_add:
        app_label = related_model._meta.app_label
        model = related_model._meta.object_name.lower()
        self.widget.add_link = reverse('admin:%s_%s_add' % (app_label, model)) + '?_popup=1'


def autoselect_fields_check_can_add(form, model, user):
    """
    Check the form's fields for any autoselect fields and enable their
    widgets with green + button if permissions allow then to create the related_model.
    """
    for name, form_field in form.declared_fields.items():
        if isinstance(form_field, (AutoCompleteSelectMultipleField, AutoCompleteSelectField)):
            db_field = model._meta.get_field(name)
            form_field.check_can_add(user, db_field.rel.to)


def make_plugin_options(lookup, channel_name, widget_plugin_options, initial):
    """ Make a JSON dumped dict of all options for the jQuery ui plugin."""
    po = {}
    if initial:
        po['initial'] = initial
    po.update(getattr(lookup, 'plugin_options', {}))
    po.update(widget_plugin_options)
    if not po.get('source'):
        po['source'] = reverse('ajax_lookup', kwargs={'channel': channel_name})

    # allow html unless explicitly set
    if po.get('html') is None:
        po['html'] = True

    return {
        'plugin_options': mark_safe(json.dumps(po)),
        'data_plugin_options': force_escape(json.dumps(po))
    }


def pack_ids(ids):
    if ids:
        # |pk|pk| of current
        return "|" + "|".join(str(pk) for pk in ids) + "|"
    else:
        return "|"
