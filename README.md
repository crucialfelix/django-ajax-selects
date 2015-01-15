
Enables editing of `ForeignKey`, `ManyToMany` and `CharField` using jQuery UI Autocomplete.

User experience
===============

selecting:

<img src='http://media.crucial-systems.com/posts/selecting.png'/>

selected:

<img src='http://media.crucial-systems.com/posts/selected.png'/>

[Note: screen shots are from the older version. Styling has changed slightly]

1. User types a few characters
2. Ajax request sent to the server
3. The dropdown menu shows choices
4. User selects by clicking or using arrow keys
5. Selected result displays in the "deck" area directly below the input field.
6. User can click trashcan icon to remove a selected item

Features
========

+ Works in any form including the Django Admin
+ Popup to add a new item
+ Admin inlines
+ Compatible with widget/form media, staticfiles, asset compressors etc.
+ Automatically Loads jQuery UI  mode allows easy installation by automatic inclusion of jQueryUI from the googleapis CDN
+ Customize HTML, CSS and JS
+ JQuery triggers allow you to customize interface behavior to respond when items are added or removed
+ Default (but customizable) security prevents griefers from pilfering your data via JSON requests



Quick Installation
==================

Get it

    `pip install django-ajax-selects`
or
    download or checkout the distribution


In settings.py :

    # add the app
    INSTALLED_APPS = (
                ...,
                'django.contrib.staticfiles',
                'ajax_select'
                )

    # define the lookup channels in use on the site
    AJAX_LOOKUP_CHANNELS = {
        #  simple: search Person.objects.filter(name__icontains=q)
        'person'  : {'model': 'example.person', 'search_field': 'name'},
        # define a custom lookup channel
        'song'   : ('example.lookups', 'SongLookup')
    }


In your urls.py:

    from django.conf.urls import *

    from django.contrib import admin
    from ajax_select import urls as ajax_select_urls

    admin.autodiscover()

    urlpatterns = patterns('',
        # include the lookup urls
        (r'^admin/lookups/', include(ajax_select_urls)),
        (r'^admin/', include(admin.site.urls)),
    )

For Django 1.3 or earlier replace the first line by `from django.conf.urls.defaults import *`.

In your admin.py:

    from django.contrib import admin
    from ajax_select import make_ajax_form
    from ajax_select.admin import AjaxSelectAdmin
    from example.models import *

    class PersonAdmin(admin.ModelAdmin):
        pass
    admin.site.register(Person,PersonAdmin)

    class LabelAdmin(AjaxSelectAdmin):
        # create an ajax form class using the factory function
        #                     model,fieldlist,   [form superclass]
        form = make_ajax_form(Label,{'owner':'person'})
    admin.site.register(Label,LabelAdmin)

example/lookups.py:

    from ajax_select import LookupChannel

    class SongLookup(LookupChannel):

        model = Song

        def get_query(self,q,request):
            return Song.objects.filter(title__icontains=q).order_by('title')


NOT SO QUICK INSTALLATION
=========================

Things that can be customized:

+ define custom `LookupChannel` classes to customize:
    + HTML formatting for the drop down results and the item-selected display
    + custom search queries, ordering, user specific filtered results
    + custom channel security (default is staff only)
+ each channel can define its own template to add controls or javascript
+ JS can respond to jQuery triggers when items are selected or removed
+ custom CSS
+ how and from where jQuery, jQueryUI, jQueryUI theme are loaded


Architecture
============

A single view services all of the ajax search requests, delegating the searches to named 'channels'.

A simple channel can be specified in settings.py, a more complex one (with custom search, formatting, personalization or auth requirements) can be written in a lookups.py file.

Each model that needs to be searched for has a channel defined for it. More than one channel may be defined for a Model to serve different needs such as public vs admin or channels that filter the query by specific categories etc. The channel also has access to the request and the user so it can personalize the query results.  Those channels can be reused by any Admin that wishes to lookup that model for a ManyToMany or ForeignKey field.



There are three model field types with corresponding form fields and widgets:

<table>
<tr><th>Database field</th><th>Form field</th><th>Form widget</th>
<tr><td>models.CharField</td><td>AutoCompleteField</td><td>AutoCompleteWidget</td></tr>
<tr><td>models.ForeignKey</td><td>AutoCompleteSelectField</td><td>AutoCompleteSelectWidget</td></tr>
<tr><td>models.ManyToManyField</td><td>AutoCompleteSelectMultipleField</td><td>AutoCompleteSelectMultipleWidget</td></tr>
</table>

Generally the helper functions documented below can be used to generate a complete form or an individual field (with widget) for a form.  In rare cases you might need to specify the ajax form field explicitly in your Form.

Example App
===========

See the example app for a full working admin site with many variations and comments. It installs quickly using virtualenv and sqllite and comes fully configured.


settings.py
-----------

#### AJAX_LOOKUP_CHANNELS

Defines the available lookup channels.

+ channel_name : {'model': 'app.modelname', 'search_field': 'name_of_field_to_search' }
> This will create a channel automatically

    channel_name : ( 'app.lookups', 'YourLookup' )
        This points to a custom Lookup channel name YourLookup in app/lookups.py

    AJAX_LOOKUP_CHANNELS = {
        #   channel : dict with settings to create a channel
        'person'  : {'model':'example.person', 'search_field':'name'},

        # channel: ( module.where_lookup_is, ClassNameOfLookup )
        'song'   : ('example.lookups', 'SongLookup'),
    }

#### AJAX_SELECT_BOOTSTRAP

By default it will include bootstrap.js in the widget media which will locate or load jQuery and jQuery-UI.

In other words, by default it will just work.

If you don't want it do that, in settings.py:
    AJAX_SELECT_BOOTSTRAP = False

First one wins:

*  window.jQuery - if you already included jQuery on the page
*  or loads: //ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js

Likewise for jQuery-UI:

* window.jQuery.ui
* or loads: //ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js
  with theme: //ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/themes/smoothness/jquery-ui.css

If you want your own custom theme then load jquery ui and your css first.

Warning: the latest jQueryUI seems to have issues with the autocomplete.  I would rather switch to the much nicer select2 than try to get the latest jQuery UI to work.  Its a lot of js and css to load just for a dropdown.


urls.py
-------

Simply include the ajax_select urls in your site's urlpatterns:

    from django.conf.urls.defaults import *

    from django.contrib import admin
    from ajax_select import urls as ajax_select_urls

    admin.autodiscover()

    urlpatterns = patterns('',
        (r'^admin/lookups/', include(ajax_select_urls)),
        (r'^admin/', include(admin.site.urls)),
    )


lookups.py
----------

By convention this is where you would define custom lookup channels

Subclass `LookupChannel` and override any method you wish to customize.

1.1x Upgrade note: previous versions did not have a parent class. The methods format_result and format_item have been renamed to format_match and format_item_display respectively.
Those old lookup channels will still work and the previous methods will be used.  It is still better to adjust your lookup channels to inherit from the new base class.

    from ajax_select import LookupChannel
    from django.utils.html import escape
    from django.db.models import Q
    from example.models import *

    class PersonLookup(LookupChannel):

        model = Person

        def get_query(self,q,request):
            return Person.objects.filter(Q(name__icontains=q) | Q(email__istartswith=q)).order_by('name')

        def get_result(self,obj):
            u""" result is the simple text that is the completion of what the person typed """
            return obj.name

        def format_match(self,obj):
            """ (HTML) formatted item for display in the dropdown """
            return self.format_item_display(obj)

        def format_item_display(self,obj):
            """ (HTML) formatted item for displaying item in the selected deck area """
            return u"%s<div><i>%s</i></div>" % (escape(obj.name),escape(obj.email))

    Note that raw strings should always be escaped with the escape() function

#### Methods you can override in your `LookupChannel`


###### model [property]

The model class this channel searches

###### plugin_options [property, default={}]

Set any options for the jQuery plugin. This includes:

+ minLength
+ autoFocus
+ disabled
+ position
+ source - setting this would overide the normal ajax URL. could be used to add URL query params

See http://docs.jquery.com/UI/Autocomplete#options

The field or widget may also specify plugin_options that will overwrite those specified by the channel.

###### min_length [property, default=1]

This is a jQuery plugin option.  It is preferred to set this in the plugin_options dict, but this older style attribute will still be honored.

Minimum query length to return a result.  Large datasets can choke if they search too often with small queries.
Better to demand at least 2 or 3 characters.
This param is also used in jQuery's UI when filtering results from its own cache.

###### search_field [property, optional]

Name of the field for the query to search with icontains.  This is used only in the default get_query implementation.
Usually better to just implement your own get_query

######  get_query(self,q,request)

return a query set searching for the query string q, ordering as appropriate.
Either implement this method yourself or set the search_field property.
Note that you may return any iterable so you can even use yield and turn this method into a generator,
or return an generator or list comprehension.

######  get_result(self,obj):

The text result of autocompleting the entered query.  This is currently displayed only for a moment in the text field
after the user has selected the item.  Then the item is displayed in the item_display deck and the text field is cleared.
Future versions may offer different handlers for how to display the selected item(s).  In the current version you may
add extra script and use triggers to customize.

######  format_match(self,obj):

(HTML) formatted item for displaying item in the result dropdown

######  format_item_display(self,obj):

(HTML) formatted item for displaying item in the selected deck area (directly below the text field).
Note that we use jQuery .position() to correctly place the deck area below the text field regardless of
whether the widget is in the admin, and admin inline or an outside form.  ie. it does not depend on django's
admin css to correctly place the selected display area.

######  get_objects(self,ids):

Get the currently selected objects when editing an existing model

Note that the order of the ids supplied for ManyToMany fields is dependent on how the objects manager fetches it.
ie. what is returned by yourmodel.fieldname_set.all()

In most situations (especially postgres) this order is random, not the order that you originally added them in the interface.  With a bit of hacking I have convinced it to preserve the order [see OrderedManyToMany.md for solution]

######  can_add(self, user, argmodel):

Check if the user has permission to add one of these models.
This enables the green popup +
Default is the standard django permission check

######  check_auth(self,request):

To ensure that nobody can get your data via json simply by knowing the URL.
The default is to limit it to request.user.is_staff and raise a PermissionDenied exception.
By default this is an error with a 401 response, but your middleware may intercept and choose to do other things.

Public facing forms should write a custom `LookupChannel` to implement as needed.
Also you could choose to return HttpResponseForbidden("who are you?") instead of raising PermissionDenied


admin.py
--------

#### make_ajax_form(model, fieldlist, superclass=ModelForm, show_help_text=False)

If your application does not otherwise require a custom Form class then you can use the make_ajax_form helper to create the entire form directly in admin.py.  See forms.py below for cases where you wish to make your own Form.

+ *model*: your model
+ *fieldlist*: a dict of {fieldname : channel_name, ... }
+ *superclass*: [default ModelForm] Substitute a different superclass for the constructed Form class.
+ *show_help_text*: [default False]
    Leave blank [False] if using this form in a standard Admin.
    Set it True for InlineAdmin classes or if making a form for use outside of the Admin.

######Example

    from ajax_select import make_ajax_form
    from ajax_select.admin import AjaxSelectAdmin
    from yourapp.models import YourModel

    class YourModelAdmin(AjaxSelectAdmin):
        # create an ajax form class using the factory function
        #                     model, fieldlist,   [form superclass]
        form = make_ajax_form(Label, {'owner': 'person'})

    admin.site.register(YourModel,YourModelAdmin)

You may use AjaxSelectAdmin as a mixin class and multiple inherit if you have another Admin class that you would like to use.  You may also just add the hook into your own Admin class:

    def get_form(self, request, obj=None, **kwargs):
        form = super(YourAdminClass, self).get_form(request, obj, **kwargs)
        autoselect_fields_check_can_add(form, self.model, request.user)
        return form

Note that ajax_selects does not need to be in an admin.  Popups will still use an admin view (the registered admin for the model being added), even if the form from where the popup was launched does not.


forms.py
--------

subclass ModelForm just as usual.  You may add ajax fields using the helper or directly.

#### make_ajax_field(model, model_fieldname, channel, show_help_text=False, **kwargs)

A factory function to makes an ajax field + widget.  The helper ensures things are set correctly and simplifies usage and imports thus reducing programmer error.  All kwargs are passed into the Field so it is no less customizable.

+ *model*:              the model that this ModelForm is for
+ *model_fieldname*:    the field on the model that is being edited (ForeignKey, ManyToManyField or CharField)
+ *channel*:            the lookup channel to use for searches
+ *show_help_text*:      [default False]  Whether to show the help text inside the widget itself.
                        When using in AdminInline or outside of the admin then set it to True.
+ *kwargs*:             Additional kwargs are passed on to the form field.
    Of interest:
        help_text="Custom help text"
    or:
        # do not show any help at all
        help_text=None

    plugin_options - directly specify jQuery plugin options.  see Lookup plugin_options above


#####Example

    from ajax_select import make_ajax_field

    class ReleaseForm(ModelForm):

        class Meta:
            model = Release

        group  = make_ajax_field(Release, 'group', 'group', help_text=None)

#### Without using the helper


    from ajax_select.fields import AutoCompleteSelectField

    class ReleaseForm(ModelForm):

        group = AutoCompleteSelectField('group', required=False, help_text=None)

#### Setting plugin options

    from ajax_select.fields import AutoCompleteSelectField

    class ReleaseForm(ModelForm):

        group = AutoCompleteSelectField('group', required=False, help_text=None, plugin_options = {'autoFocus': True, 'minLength': 4})

#### Using ajax selects in a `FormSet`

There is possibly a better way to do this, but here is an initial example:

`forms.py`

    from django.forms.models import modelformset_factory
    from django.forms.models import BaseModelFormSet
    from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

    from models import *

    # create a superclass
    class BaseTaskFormSet(BaseModelFormSet):

        # that adds the field in, overwriting the previous default field
        def add_fields(self, form, index):
            super(BaseTaskFormSet, self).add_fields(form, index)
            form.fields["project"] = AutoCompleteSelectField('project', required=False)

    # pass in the base formset class to the factory
    TaskFormSet = modelformset_factory(Task, fields=('name', 'project', 'area'),extra=0, formset=BaseTaskFormSet)



templates/
----------

Each form field widget is rendered using a template.  You may write a custom template per channel and extend the base template in order to implement these blocks:

    {% block extra_script %}{% endblock %}
    {% block help %}{% endblock %}

<table>
    <tr><th>form Field</th><th>tries this first</th><th>default template</th></tr>
    <tr><td>AutoCompleteField</td><td>templates/autocomplete_{{CHANNELNAME}}.html</td><td>templates/autocomplete.html</td></tr> <tr><td>AutoCompleteSelectField</td><td>templates/autocompleteselect_{{CHANNELNAME}}.html</td><td>templates/autocompleteselect.html</td></tr>
 <tr><td>AutoCompleteSelectMultipleField</td><td>templates/autocompleteselectmultiple_{{CHANNELNAME}}.html</td><td>templates/autocompleteselectmultiple.html</td></tr>
</table>

See ajax_select/static/js/ajax_select.js below for the use of jQuery trigger events


ajax_select/static/css/ajax_select.css
--------------------------------------

If you are using `django.contrib.staticfiles` then you can implement `ajax_select.css` and put your app ahead of ajax_select to cause it to be collected by the management command `collectfiles`.

If you are doing your own compress stack then of course you can include whatever version you want.

The display style now uses the jQuery UI theme and actually I find the drop down to be not very charming.  The previous version (1.1x) which used the external jQuery AutoComplete plugin had nicer styling.  I might decide to make the default more like that with alternating color rows and a stronger sense of focused item.  Also the current jQuery one wiggles.

The trashcan icon comes from the jQueryUI theme by the css classes:

    "ui-icon ui-icon-trash"

The css declaration:

    .results_on_deck .ui-icon.ui-icon-trash { }

would be "stronger" than jQuery's style declaration and thus you could make trash look less trashy.


ajax_select/static/js/ajax_select.js
------------------------------------

You probably don't want to mess with this one.  But by using the extra_script block as detailed in templates/ above you can add extra javascript, particularily to respond to event Triggers.

Triggers are a great way to keep code clean and untangled. see: http://docs.jquery.com/Events/trigger

Two triggers/signals are sent: 'added' and 'killed'. These are sent to the $("#{{html_id}}_on_deck") element. That is the area that surrounds the currently selected items.

Extend the template, implement the extra_script block and bind functions that will respond to the trigger:

##### multi select:

    {% block extra_script %}
        $("#{{html_id}}_on_deck").bind('added',function() {
                id = $("#{{html_id}}").val();
                alert('added id:' + id );
        });
        $("#{{html_id}}_on_deck").bind('killed',function() {
                current = $("#{{html_id}}").val()
                alert('removed, current is:' + current);
        });
    {% endblock %}

##### select:

    {% block extra_script %}
        $("#{{html_id}}_on_deck").bind('added',function() {
                id = $("#{{html_id}}").val();
                alert('added id:' + id );
        });
        $("#{{html_id}}_on_deck").bind('killed',function() {
                alert('removed');
        });
    {% endblock %}

##### auto-complete text field:

    {% block extra_script %}
        $('#{{ html_id }}').bind('added',function() {
                entered = $('#{{ html_id }}').val();
                alert( entered );
        });
    {% endblock %}

There is no remove as there is no kill/delete button in a simple auto-complete.
The user may clear the text themselves but there is no javascript involved. Its just a text field.


Contributors
------------

Many thanks to all who found bugs, asked for things, and hassled me to get a new release out.  I'm glad people find good use out of the app.

In particular thanks for help in the 1.2 version:  @sjrd (Sébastien Doeraene)
And much thanks to @brianmay for assistance over many releases.


License
-------

Dual licensed under the MIT and GPL licenses:
   http://www.opensource.org/licenses/mit-license.php
   http://www.gnu.org/licenses/gpl.html
