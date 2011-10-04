
from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from example.forms import ReleaseForm
from example.models import *



class PersonAdmin(admin.ModelAdmin):

    pass
    
admin.site.register(Person,PersonAdmin)



class LabelAdmin(AjaxSelectAdmin):
    """ to get + popup buttons, subclass AjaxSelectAdmin 
        multi-inheritance also possible:  
    
        class PersonAdmin(YourAdminSuperclass,AjaxSelectAdmin):
    """
    # create an ajax form class using the factory function
    #                     model,fieldlist,   [form superclass]
    form = make_ajax_form(Label,{'owner':'person'})

admin.site.register(Label,LabelAdmin)



class GroupAdmin(admin.ModelAdmin):

    form = make_ajax_form(Group,{'members':'person'})

admin.site.register(Group,GroupAdmin)



class SongAdmin(admin.ModelAdmin):

    form = make_ajax_form(Song,{'group':'group'})

admin.site.register(Song,SongAdmin)



class ReleaseAdmin(AjaxSelectAdmin):

    # specify a form class manually (normal django way)
    # see forms.py
    form = ReleaseForm

admin.site.register(Release,ReleaseAdmin)



