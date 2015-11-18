Release Notes
=============


1.4.0
=====

- Autodiscover of lookups.py for Django 1.7+
- Simpler configuration
- Fix support for Django 1.8, Python 3
- Support for Django 1.9b1
- Add full testing matrix
- New clearer multi-page documentation
- Extensive docstrings
- Support form reset button

fix: changed_data always includes AutoComplete fields

Breaking Changes
----------------

**Custom templates**

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


**No more conversion of values by Widget**

Previous releases would try to convert the primary key submitted from the Widget into either an integer or string,
depending on what it looked like. This was to support databases with non-integer primary keys.

Its best that the Widget does not involve itself with the database types, it should only process its input.

Django's ORM converts strings to integers. If for some reason your database is getting the wrong type for a PK,
then you should handle this conversion in your Form's clean_fieldname method.

**Removed deprecated options**

`make_ajax_field`: dropped backward compat support for `show_m2m_help` option.
Use `show_help_text`.

remove deprecated `min_length` template var - use `plugin_options['min_length']`
remove deprecated `lookup_url` template var - use `plugin_options['source']`


**settings**

LookupChannels are still loaded from `settings.AJAX_LOOKUP_CHANNELS` as previously.

If you are on Django >= 1.7 you may switch to using the @register decorator and you can probably remove `AJAX_LOOKUP_CHANNELS` entirely.


1.3.6
=============

Support for Django 1.8

1.3.5
=============

Support for Django 1.7
Support for non-integer primary keys

1.3.4
=============

Fix protocols removing http/https in bootstrap

1.3.2
=============

Fixed issues with bootstrap.js correctly detecting the presence of jQuery.ui.autocomplete


1.3
===========

+ Support for Django 1.5 and 1.6
+ Assets moved so that staticfiles works correctly
+ Media classes for widgets added so that Form and Admin media work correctly
+ Spinner image is now served locally, no from github (since staticfiles works now)
+ Improved bootstrap.js that locates or CDN loads a jQuery and a jQuery-ui as needed
+ XSS vulnerability patched in the default lookup

+ Inline scripts moved out of html.
	Form fields are activated after the body is loaded with plugin settings stored in the field's data-plugin-options.
	This means that javascript including jquery can be at the bottom of the page.
	Also less html, more resuable javascript.

+ max-width hack removed
	This set the max-width of the dropdown menu for autocomplete fields (simple text) to the size of the text field.
	Dropdowns are now the min-width of the text field and max width of 60% of parent div.
	This works well in Django admin, in pop ups and in narrow pages.


Breaking changes
----------------

The widget templates no longer have any javascript in them.  If you have custom templates you can simplify them now.

The extra_script block is retained in case you are extending a template (to add custom triggers) but it is no longer inside a `jQuery.ready(function() {  })` block, so if you are using it then you will need to wrap your code in one.

The bootstrap script uses Django staticfiles

AJAX_SELECT_BOOTSTRAP defaults to True now
