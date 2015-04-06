
Version 1.3.6
=============

Support for Django 1.8

Version 1.3.5
=============

Support for Django 1.7
Support for non-integer primary keys

Version 1.3.4
=============

Fix protocols removing http/https in bootstrap

Version 1.3.2
=============

Fixed issues with bootstrap.js correctly detecting the presence of jQuery.ui.autocomplete


Version 1.3
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
