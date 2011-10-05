

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
        u""" result is the simple text that is the completion of what the person typed """
        return obj.name

    def get_objects(self,ids):
        # simplest, just return them:
        # return Person.objects.filter(id__in=ids)
        
        # return in the original ordering as added to the interface when last edited:
        ids = [int(id) for id in ids]
        persons = dict( (a.pk,a) for a in Person.objects.filter(pk__in=ids) )
        return [persons[aid] for aid in ids if persons.has_key(aid)]

    def can_add(self,user,model):
        """ could check if user has sufficient privileges. 
            only those allowed to add will be offered a [+ add] """
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


class ClicheLookup(object):
    
    """ an autocomplete lookup does not need to search models
        though the words here could also be stored in a model and
        searched as in the lookups above 
        """
        
    words = [
        u"rain cats and dogs",
        u"quick as a cat",
        u"there's more than one way to skin a cat",
        u"let the cat out of the bag",
        u"fat cat",
        u"the early bird catches the worm",
        u"catch as catch can",
        u"you can catch more flies with honey than with vinegar",
        u"catbird seat",
        u"cat's paw",
        u"cat's meow",
        u"has the cat got your tongue?",
        u"busy as a cat on a hot tin roof",
        u"who'll bell the cat",
        u"cat's ass",
        u"more nervous than a long tailed cat in a room full of rocking chairs",
        u"all cats are grey in the dark",
        u"nervous as a cat in a room full of rocking chairs",
        u"can't a cat look at a queen?",
        u"curiosity killed the cat",
        u"cat's pajamas",
        u"look what the cat dragged in",
        u"while the cat's away the mice will play",
        u"Nervous as a cat in a room full of rocking chairs",
        u"Slicker than cat shit on a linoleum floor",
        u"there's more than one way to kill a cat than choking it with butter.",
        u"you can't swing a dead cat without hitting one",
        u"The cat's whisker",
        u"looking like the cat who swallowed the canary",
        u"not enough room to swing a cat",
        u"It's raining cats and dogs",
        u"He was on that like a pack of dogs on a three-legged cat.",
        u"like two tomcats in a gunny sack",
        u"I don't know your from adam's house cat!",
        u"Crazier than Joe Cunt's cat",
        u"nervous as a long tailed cat in a living room full of rockers",
        u"Busier than a three legged cat in a dry sand box.",
        u"Busier than a one-eyed cat watching two mouse holes.",
        u"kick the dog and cat",
        u"there's more than one way to kill a cat than to drown it in cream",
        u"how many ways can you skin a cat?",
        u"Looks like a black cat with a red bird in its mouth",
        u"Morals of an alley cat and scruples of a snake.",
        u"hotter than a six peckered alley cat",
        u"when the cats are away the mice will play",
        u"you can catch more flies with honey than vinegar",
        u"when the cat's away, the mice will play",
        u"Who opened the cattleguard?",
        u"your past might catch up with you",
        u"ain't that just the cats pyjamas",
        u"A Cat has nine lives",
        u"a cheshire-cat smile",
        u"cat's pajamas",
        u"cat got your tongue?"]

    def get_query(self,q,request):
        return sorted([w for w in self.words if q in w])

    def format_item(self,word):
        return word

    def format_result(self,word):
        return word

