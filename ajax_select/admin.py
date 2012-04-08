

from ajax_select.fields import autoselect_fields_check_can_add
from django.contrib import admin
from django.conf import settings

class AjaxSelectAdmin(admin.ModelAdmin):

    """ in order to get + popup functions subclass this or do the same hook inside of your get_form """

    def get_form(self, request, obj=None, **kwargs):
        form = super(AjaxSelectAdmin,self).get_form(request,obj,**kwargs)
        
        autoselect_fields_check_can_add(form,self.model,request.user)

        class Media:
            css = {
             'all': ('ajax_select/jquery/css/ui-lightness/jquery-ui-1.8.18.custom.css',),
            }
            js = ('ajax_select/jquery/js/jquery-1.7.1.min.js', 'ajax_select/jquery/js/jquery-ui-1.8.18.custom.min.js')

        if settings.AJAX_SELECT_INLINES == 'staticfiles':
            setattr(form, 'Media', Media)

        return form

