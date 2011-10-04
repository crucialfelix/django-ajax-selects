

from example.models import *
from django.db.models import Q


class PersonLookup(object):

    def get_query(self,q,request):
        return Person.objects.filter(Q(name__icontains=q) | Q(email__istartswith=q)).order_by('name')

    def format_item(self,obj):
        """ item can be formatted and is shown in the autocomplete dropdown
            and after the item is selected and shown below the input """
        return "%s<div><i>%s</i></div>" % (obj.name,obj.email)

    def format_result(self,obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.name

    def get_objects(self,ids):
        # return Person.objects.filter(id__in=ids)
        # return in original ordering as added to interface:
        ids = [int(id) for id in ids]
        persons = dict( (a.pk,a) for a in Person.objects.filter(pk__in=ids) )
        return [persons[aid] for aid in ids if persons.has_key(aid)]

    def can_add(self,user,model):
        return True


class GroupLookup(object):

    def get_query(self,q,request):
        return Group.objects.filter(name__icontains=q).order_by('name')

    def format_item(self,obj):
        return "%s<div><i>%s</i></div>" % (obj.name,obj.url)

    def format_result(self,obj):
        return obj.name

    def get_objects(self,ids):
        return Group.objects.filter(id__in=ids)

    def can_add(self,user,model):
        return True


# uses the ez lookup creation method. see settings.py
# class LabelLookup(object):

#     def get_query(self,q,request):
#         return Label.objects.filter(name__icontains=q).order_by('name')

#     def format_item(self,obj):
#         return "%s<div><i>%s</i></div>" % (obj.name,obj.url)

#     def format_result(self,obj):
#         return obj.name

#     def get_objects(self,ids):
#         return Label.objects.filter(id__in=ids)

#     def can_add(self,user,model):
#         return True


class SongLookup(object):

    def get_query(self,q,request):
        return Song.objects.filter(title__icontains=q).select_related('group').order_by('title')

    def format_item(self,obj):
        return "%s<div><i>by %s</i></div>" % (obj.name,obj.group.name)

    def format_result(self,obj):
        return obj.name

    def get_objects(self,ids):
        return Song.objects.filter(id__in=ids)

    def can_add(self,user,model):
        return True

