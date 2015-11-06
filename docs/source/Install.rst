Install
=======

Install::

    pip install django-ajax-selects

Add the app::

    # settings.py
    INSTALLED_APPS = (
        ...
        'ajax_select',  # <-   add the app
        ...
    )

Include the urls in your project::

    # urls.py
    from django.conf.urls import url, include
    from django.conf.urls.static import static
    from django.contrib import admin
    from django.conf import settings
    from ajax_select import urls as ajax_select_urls

    admin.autodiscover()

    urlpatterns = [

        # place it at whatever base url you like
        url(r'^ajax_select/', include(ajax_select_urls)),

        url(r'^admin/', include(admin.site.urls)),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


Write a LookupChannel to specify the models, search queries, formatting etc. and register it with a channel name::

      from ajax_select import register, LookupChannel
      from .models import Tag

      @register('tags')
      class TagsLookup(LookupChannel):

          model = Tag

          def get_query(self, q, request):
              return self.model.objects.filter(name=q)

          def format_item_display(self, item):
              return u"<span class='tag'>%s</span>" % item.name

If you are using Django >= 1.7 then it will automatically loaded on startup.
For previous Djangos you can import them manually to your urls or views.

Add ajax lookup fields in your admin.py::

    from django.contrib import admin
    from ajax_select import make_ajax_form
    from .models import Document

    @admin.register(Document)
    class DocumentAdmin(AjaxSelectAdmin):

        form = make_ajax_form(Document, {
            # fieldname: channel_name
            'tags': 'tags'
        })

Or add the fields to a ModelForm::

    # forms.py
    from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

    class DocumentForm(ModelForm):

        class Meta:
            model = Document

        category = AutoCompleteSelectField('categories', required=False, help_text=None)
        tags = AutoCompleteSelectMultipleField('tags', required=False, help_text=None)

    # admin.py
    from django.contrib import admin
    from .forms import DocumentForm
    from .models import Document

    @admin.register(Document)
    class DocumentAdmin(AjaxSelectAdmin):
        form = DocumentForm
