Forms
=====

Forms can be used either for an Admin or in normal Django views.

Subclass ModelForm as usual and define fields::

    from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

    class DocumentForm(ModelForm):

        class Meta:
            model = Document

        category = AutoCompleteSelectField('categories', required=False, help_text=None)
        tags = AutoCompleteSelectMultipleField('tags', required=False, help_text=None)


make_ajax_field
---------------

There is also a helper method available here.

.. automodule:: ajax_select.helpers
  :members: make_ajax_field
  :noindex:


Example::

    from ajax_select import make_ajax_field

    class DocumentForm(ModelForm):

        class Meta:
            model = Document

        category  = make_ajax_field(Category, 'categories', 'category', help_text=None)
        tags  = make_ajax_field(Tag, 'tags', 'tags', help_text=None)



FormSet
-------

There is possibly a better way to do this, but here is an initial example:

`forms.py`::

    from django.forms.models import modelformset_factory
    from django.forms.models import BaseModelFormSet
    from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

    from models import Task

    # create a superclass
    class BaseTaskFormSet(BaseModelFormSet):

        # that adds the field in, overwriting the previous default field
        def add_fields(self, form, index):
            super(BaseTaskFormSet, self).add_fields(form, index)
            form.fields["project"] = AutoCompleteSelectField('project', required=False)

    # pass in the base formset class to the factory
    TaskFormSet = modelformset_factory(Task, fields=('name', 'project', 'area'), extra=0, formset=BaseTaskFormSet)
