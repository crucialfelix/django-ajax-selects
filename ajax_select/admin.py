from django.contrib import admin
from ajax_select.fields import autoselect_fields_check_can_add


class AjaxSelectAdmin(admin.ModelAdmin):

    """ in order to get + popup functions subclass this or do the same hook inside of your get_form """

    def get_form(self, request, obj=None, **kwargs):
        form = super(AjaxSelectAdmin, self).get_form(request, obj, **kwargs)

        autoselect_fields_check_can_add(form, self.model, request.user)
        return form


class AjaxSelectAdminInlineFormsetMixin(object):

    def get_formset(self, request, obj=None, **kwargs):
        fs = super(AjaxSelectAdminInlineFormsetMixin, self).get_formset(request, obj, **kwargs)
        autoselect_fields_check_can_add(fs.form, self.model, request.user)
        return fs


class AjaxSelectAdminTabularInline(AjaxSelectAdminInlineFormsetMixin, admin.TabularInline):
    pass


class AjaxSelectAdminStackedInline(AjaxSelectAdminInlineFormsetMixin, admin.StackedInline):
    pass
