jQuery Plugin Options
=====================


https://jqueryui.com/autocomplete/

- minLength
  The minimum number of characters a user must type before a search is performed.
  min_length is also an attribute of the LookupChannel so you need to also set it there.
- autoFocus
- delay
- disabled
- position
- source - By default this is the ajax_select view.
  Setting this would overide the normal url used for lookups (`ajax_select.views.ajax_lookup`). This could be used to add URL custom query params.

See http://docs.jquery.com/UI/Autocomplete#options


Setting plugin options::

    from ajax_select.fields import AutoCompleteSelectField

    class DocumentForm(ModelForm):

        category = AutoCompleteSelectField('category',
            required=False,
            help_text=None,
            plugin_options={'autoFocus': True, 'minLength': 4})

This Python dict will be passed as JavaScript to the plugin.
