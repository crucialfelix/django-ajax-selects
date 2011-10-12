

from django.db.models import Q
from django.utils.html import escape
from example.models import *
from ajax_select import LookupChannel


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



class GroupLookup(LookupChannel):

    model = Group

    def get_query(self,q,request):
        return Group.objects.filter(name__icontains=q).order_by('name')

    def get_result(self,obj):
        return unicode(obj)
        
    def format_match(self,obj):
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        return u"%s<div><i>%s</i></div>" % (escape(obj.name),escape(obj.url))

    def can_add(self,user,model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True


class SongLookup(LookupChannel):

    model = Song

    def get_query(self,q,request):
        return Song.objects.filter(title__icontains=q).select_related('group').order_by('title')

    def get_result(self,obj):
        return unicode(obj.title)
        
    def format_match(self,obj):
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        return "%s<div><i>by %s</i></div>" % (escape(obj.title),escape(obj.group.name))



class ClicheLookup(LookupChannel):

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

    def get_result(self,obj):
        return obj

    def format_match(self,obj):
        return escape(obj)

    def format_item_display(self,obj):
        return escape(obj)

