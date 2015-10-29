from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.models import ModelForm
from django.utils.text import capfirst
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


def make_ajax_form(model, fieldlist, superclass=ModelForm, show_help_text=False, **kwargs):
    """ Creates a ModelForm subclass with autocomplete fields

        usage:
            class YourModelAdmin(Admin):
                ...
                form = make_ajax_form(YourModel,{'contacts':'contact','author':'contact'})

        where
            'contacts' is a ManyToManyField specifying to use the lookup channel 'contact'
        and
            'author' is a ForeignKeyField specifying here to also use the lookup channel 'contact'
    """
    # will support previous arg name for several versions before deprecating
    # TODO: time to go
    if 'show_m2m_help' in kwargs:
        show_help_text = kwargs.pop('show_m2m_help')

    class TheForm(superclass):

        class Meta:
            exclude = []

        setattr(Meta, 'model', model)
        if hasattr(superclass, 'Meta'):
            if hasattr(superclass.Meta, 'fields'):
                setattr(Meta, 'fields', superclass.Meta.fields)
            if hasattr(superclass.Meta, 'exclude'):
                setattr(Meta, 'exclude', superclass.Meta.exclude)
            if hasattr(superclass.Meta, 'widgets'):
                setattr(Meta, 'widgets', superclass.Meta.widgets)

    for model_fieldname, channel in fieldlist.items():
        f = make_ajax_field(model, model_fieldname, channel, show_help_text)

        TheForm.declared_fields[model_fieldname] = f
        TheForm.base_fields[model_fieldname] = f

    return TheForm


def make_ajax_field(model, model_fieldname, channel, show_help_text=False, **kwargs):
    """ Makes a single autocomplete field for use in a Form

        optional args:
            help_text - default is the model db field's help_text.
                None will disable all help text
            label     - default is the model db field's verbose name
            required  - default is the model db field's (not) blank

            show_help_text -
                Django will show help text below the widget, but not for ManyToMany inside of admin inlines
                This setting will show the help text inside the widget itself.
    """
    # will support previous arg name for several versions before deprecating
    # TODO remove this now
    if 'show_m2m_help' in kwargs:
        show_help_text = kwargs.pop('show_m2m_help')

    from ajax_select.fields import AutoCompleteField, \
                                   AutoCompleteSelectMultipleField, \
                                   AutoCompleteSelectField

    field = model._meta.get_field(model_fieldname)
    if 'label' not in kwargs:
        kwargs['label'] = _(capfirst(force_text(field.verbose_name)))

    if ('help_text' not in kwargs) and field.help_text:
        kwargs['help_text'] = field.help_text
    if 'required' not in kwargs:
        kwargs['required'] = not field.blank

    kwargs['show_help_text'] = show_help_text
    if isinstance(field, ManyToManyField):
        f = AutoCompleteSelectMultipleField(
            channel,
            **kwargs)
    elif isinstance(field, ForeignKey):
        f = AutoCompleteSelectField(
            channel,
            **kwargs)
    else:
        f = AutoCompleteField(
            channel,
            **kwargs)
    return f
