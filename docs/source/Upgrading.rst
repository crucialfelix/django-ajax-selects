Upgrading from previous versions
================================

1.4

Custom Templates
----------------

Move your custom templates from::

    yourapp/templates/channel_autocomplete.html
    yourapp/templates/channel_autocompleteselect.html
    yourapp/templates/channel_autocompleteselectmultiple.html

to::

    yourapp/templates/ajax_select/channel_autocomplete.html
    yourapp/templates/ajax_select/channel_autocompleteselect.html
    yourapp/templates/ajax_select/channel_autocompleteselectmultiple.html

And change your extends from::

    {% extends "autocompleteselect.html" %}

to::

    {% extends "ajax_select/autocompleteselect.html" %}


Removed options
---------------

make_ajax_field:
  show_m2m_help -> show_help_text

settings
--------

LookupChannels are still loaded from `settings.AJAX_LOOKUP_CHANNELS` as previously.

If you are on Django >= 1.7 you may switch to using the @register decorator and you can remove that setting.
