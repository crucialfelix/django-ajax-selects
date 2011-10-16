
Enables editing of `ForeignKey`, `ManyToMany` and `CharField´ using jQuery UI Autocomplete.

User experience
===============

selecting:

<img src='http://media.crucial-systems.com/posts/selecting.png'/>

selected:

<img src='http://media.crucial-systems.com/posts/selected.png'/>

The user types a search term into the text field, an ajax request is sent to the server. The dropdown menu is populated with results. The user selects by clicking or using arrow keys and the selected result displays in the "deck" area directly below the input field.

Rich formatting can be easily defined for the dropdown display and the selected "deck" display.
Popup to add a new item is supported
Admin inlines now supported
Ajax Selects works in the admin and also in public facing forms.
Templates and CSS are customizable
JQuery triggers enable you to add javascript to respond when items are added or removed, so other interface elements on the page can be manipulated.
Boostrap mode allows automatic inclusion of jQueryUI from the googleapis CDN
Compatible with staticfiles, appmedia, django-compressor etc
Default security

*Django 1.2+*


Architecture
============

A single view services all of the ajax search requests, delegating the searches to named 'channels'.  Each model that needs to be searched for has a channel defined for it.

A simple channel can be specified in settings.py, a more complex one (with custom search, formatting or auth requirements) can be written in a lookups.py file.


Installation
============

Easiest
=======

In settings.py :

    # add the app
    INSTALLED_APPS = (
                ...,
                'ajax_select'
                )

    # define the lookup channels in use on the site
    AJAX_LOOKUP_CHANNELS = {
        #   pass a dict with the model and field to search against
        'person'  : {'model':'example.person', 'search_field':'name'}
    }
    # magically include jqueryUI/js/css
    AJAX_SELECT_BOOTSTRAP = True
    AJAX_SELECT_INLINES = 'inline'

In your urls.py:

    from django.conf.urls.defaults import *

    from django.contrib import admin
    from ajax_select import urls as ajax_select_urls

    admin.autodiscover()

    urlpatterns = patterns('',
        # include the lookup urls
        (r'^admin/lookups/', include(ajax_select_urls)),
        (r'^admin/', include(admin.site.urls)),
    )

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


Using AJAX_SELECT_BOOTSTRAP and AJAX_SELECT_INLINES you can be up and running in minutes.  This will include redundant css/js for each form field. In most small sites this is not an issue.  If you have very large formsets and your admin site is heavily trafficked or you are using the forms on the public site then you will want to set AJAX_SELECT_INLINES = None [the default] and include the js and css using staticfiles or by adding them to your admin's compressor stack.


CUSTOM CHANNELS
===============

A channel is a simple class that handles the actual searching, defines how you want to treat the query input
(split first name and last name, which fields to search etc.) and returns id and formatted results back
to the view which sends it to the browser.

For instance the search channel 'contacts' would search for Contact models.
The class would be named ContactLookup. This channel can be used for both AutoCompleteSelect (foreign key, single item)
and AutoCompleteSelectMultiple (many-to-many) fields.

A channel is generated automatically:

    AJAX_LOOKUP_CHANNELS = {
        #   pass a dict with the model and field to search against
        'person'  : {'model':'example.person', 'search_field':'name'}
    } 

Custom search channels can be written when you need to do a more complex search, check the user's permissions,
format the results differently or customize the sort order of the results.


_peoplez/lookups.py_

    from peoplez.models import Contact
    from django.db.models import Q
    from django.utils.html import escape
    from ajax_select import LookupChannel

    class ContactLookup(LookupChannel):

        # Minimum number of characters that must be input to trigger the AJAX query.
        # Optional, defaults to 1. 0 is a valid value.
        min_length = 2

        def get_query(self,q,request):
            """ return a query set.  you also have access to request.user if you want to for instance search 
                the current users personal contact list. """
            return Contact.objects.filter(Q(name__istartswith=q) | Q(fname__istartswith=q) | Q(lname__istartswith=q) | Q(email__icontains=q))

        def get_result(self,contact):
            """ The text result of autocompleting the entered query """
            return escape(u"%s %s %s (%s)" % (contact.fname, contact.lname,contact.name,contact.email))

        def format_item_display(self,contact):
            """ (HTML) formatted item for displaying item in the selected deck area """
            return escape(unicode(contact))

        def format_match(self,contact):
            """ (HTML) formatted item for displaying item in the selected deck area """
            return escape(unicode(contact))

        def get_objects(self,ids):
            """ given a list of ids, return the objects ordered as you would like them on the admin page.
                this is for displaying the currently selected items (in the case of a ManyToMany field)
            """
            return Contact.objects.filter(pk__in=ids).order_by('name','lname')


HTML is fine in the result or item format. Raw data should be escaped with the escape() function.

Include the urls in your site's `urls.py`. This adds the lookup view and the pop up admin view.
    (r'^ajax_select/', include('ajax_select.urls')),


##It you want to use django-ajax-select in your admin page,

for an example model:


    class ContactMailing(models.Model):
        """ can mail to multiple contacts, has one author """
        contacts = models.ManyToManyField(Contact, blank=True)
        author = models.ForeignKey(Contact, blank=False)
        ...

In the `admin.py` for this app:

    from ajax_select import make_ajax_form

    class ContactMailingAdmin(Admin):
        form = make_ajax_form(ContactMailing, {'author': 'contact', contacts='contact'))

`make_ajax_form( model, fieldlist)` is a factory function which will insert the ajax powered form field inputs
so in this example the `author` field (`ForeignKey`) uses the 'contact' channel and the `contacts` field (`ManyToMany`)
also uses the 'contact' channel


If you need to write your own form class then specify that form for the admin as usual:


    from forms import ContactMailingForm

    class ContactMailingAdmin(admin.ModelAdmin):
        form = ContactMailingForm

    admin.site.register(ContactMailing,ContactMailingAdmin)


in `forms.py` for that app:

    from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

    class ContactMailingForm(models.ModelForm):
        # declare a field and specify the named channel that it uses
        contacts = AutoCompleteSelectMultipleField('contact', required=False)
        author = AutoCompleteSelectField('contact', required=False)
        
        class Meta:
            model = Contact

##Using ajax selects in a `FormSet`

There might be a better way to do this.

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
    TaskFormSet = modelformset_factory(Task,fields=('name','project','area'),extra=0,formset=BaseTaskFormSet)




##Help text

If you are using AutoCompleteSelectMultiple outside of the admin then pass in `show_help_text=True`. 
This is because the admin displays the widget's help text and the widget would also.
But when used outside of the admin you need the help text. This is not the case for `AutoCompleteSelect`.

            
                    Django will append the widget help text: 
                        'Hold down Command to select more than one'
                    to your model field's help in a ManyToManyField
                    AutoCompleteSelectMultipleField monkey patches this to remove and 
                    replace it with the default help for a



##bootstrap

	If you put add your own jQuery, jQuery.ui and theme in the HEAD then it will not load
	this jQuery.ui and default theme here.


##License

Dual licensed under the MIT and GPL licenses:
   http://www.opensource.org/licenses/mit-license.php
   http://www.gnu.org/licenses/gpl.html
