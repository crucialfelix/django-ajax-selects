from __future__ import unicode_literals
from django.utils.six import text_type
from django.db.models import Q
from django.utils.html import escape
from example.models import Person, Group, Song
from ajax_select import LookupChannel
import ajax_select


class PersonLookup(LookupChannel):

    model = Person

    def get_query(self, q, request):
        return Person.objects.filter(Q(name__icontains=q) | Q(email__istartswith=q)).order_by('name')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.email))


class GroupLookup(LookupChannel):

    model = Group

    def get_query(self, q, request):
        return Group.objects.filter(name__icontains=q).order_by('name')

    def get_result(self, obj):
        return text_type(obj)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return "%s<div><i>%s</i></div>" % (escape(obj.name), escape(obj.url))

    def can_add(self, user, model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True


class SongLookup(LookupChannel):

    model = Song

    def get_query(self, q, request):
        return Song.objects.filter(title__icontains=q).select_related('group').order_by('title')

    def get_result(self, obj):
        return text_type(obj.title)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return "%s<div><i>by %s</i></div>" % (escape(obj.title), escape(obj.group.name))


# Here using decorator syntax rather than settings.AJAX_LOOKUP_CHANNELS
@ajax_select.register('cliche')
class ClicheLookup(LookupChannel):

    """ an autocomplete lookup does not need to search models
        though the words here could also be stored in a model and
        searched as in the lookups above
        """

    words = [
        "rain cats and dogs",
        "quick as a cat",
        "there's more than one way to skin a cat",
        "let the cat out of the bag",
        "fat cat",
        "the early bird catches the worm",
        "catch as catch can as catch as catch can as catch as catch can as catch as catch "
        "can as catch as catch can as catch as catch can as catch as catch can as catch as "
        "catch can as catch as catch can as catch as catch can as catch as catch can as catch "
        "as catch can as catch as catch can as catch as catch can as catch as catch can as "
        "catch as catch can as catch as catch can as catch as catch can as catch as catch "
        "can as catch as catch can as catch as catch can as catch as catch can as catch "
        "as catch can as catch as catch can as catch as catch can as catch as catch can "
        "as catch as catch can as catch as catch can as catch as catch can as catch as "
        "catch can as catch as catch can as catch as catch can as catch as catch can as "
        "catch as catch can as catch as catch can as catch as catch can as catch as catch "
        "can as catch as catch can as catch as catch can as catch as catch can as catch "
        "as catch can as catch as catch can as catch as catch can as catch as catch can "
        "as catch as catch can as catch as catch can as can",
        "you can catch more flies with honey than with vinegar",
        "catbird seat",
        "cat's paw",
        "cat's meow",
        "has the cat got your tongue?",
        "busy as a cat on a hot tin roof",
        "who'll bell the cat",
        "cat's ass",
        "more nervous than a long tailed cat in a room full of rocking chairs",
        "all cats are grey in the dark",
        "nervous as a cat in a room full of rocking chairs",
        "can't a cat look at a queen?",
        "curiosity killed the cat",
        "cat's pajamas",
        "look what the cat dragged in",
        "while the cat's away the mice will play",
        "Nervous as a cat in a room full of rocking chairs",
        "Slicker than cat shit on a linoleum floor",
        "there's more than one way to kill a cat than choking it with butter.",
        "you can't swing a dead cat without hitting one",
        "The cat's whisker",
        "looking like the cat who swallowed the canary",
        "not enough room to swing a cat",
        "It's raining cats and dogs",
        "He was on that like a pack of dogs on a three-legged cat.",
        "like two tomcats in a gunny sack",
        "I don't know your from adam's house cat!",
        "nervous as a long tailed cat in a living room full of rockers",
        "Busier than a three legged cat in a dry sand box.",
        "Busier than a one-eyed cat watching two mouse holes.",
        "kick the dog and cat",
        "there's more than one way to kill a cat than to drown it in cream",
        "how many ways can you skin a cat?",
        "Looks like a black cat with a red bird in its mouth",
        "Morals of an alley cat and scruples of a snake.",
        "hotter than a six peckered alley cat",
        "when the cats are away the mice will play",
        "you can catch more flies with honey than vinegar",
        "when the cat's away, the mice will play",
        "Who opened the cattleguard?",
        "your past might catch up with yo",
        "ain't that just the cats pyjamas",
        "A Cat has nine lives",
        "a cheshire-cat smile",
        "cat's pajamas",
        "cat got your tongue?"]

    def get_query(self, q, request):
        return sorted([w for w in self.words if q in w])

    def get_result(self, obj):
        return obj

    def format_match(self, obj):
        return escape(obj)

    def format_item_display(self, obj):
        return escape(obj)
