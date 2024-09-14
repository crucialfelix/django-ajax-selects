"""
Testing the register and autoloading.

Should not be used by other tests.
"""

from django.contrib.auth.models import User
from django.utils.html import escape

import ajax_select
from tests.models import Author, Person, PersonWithTitle


@ajax_select.register("person")
class PersonLookup(ajax_select.LookupChannel):
    model = Person

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return f"{escape(obj.name)}<div><i>{escape(obj.email)}</i></div>"

    def format_item_display(self, obj):
        return f"{escape(obj.name)}<div><i>{escape(obj.email)}</i></div>"


@ajax_select.register("person-with-title")
class PersonWithTitleLookup(ajax_select.LookupChannel):
    model = PersonWithTitle

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q)

    def get_result(self, obj):
        return f"{obj.name} {obj.title}"


@ajax_select.register("user")
class UserLookup(ajax_select.LookupChannel):
    """
    Test if you can unset a lookup provided by a third-party application.
    In this case it exposes User without any auth checking
    and somebody could manually check the ajax URL and find out
    if a user email exists.
    So you might want to turn this channel off
    by settings.AJAX_LOOKUP_CHANNELS['user'] = None.
    """

    model = User

    def get_query(self, q, request):
        return self.model.objects.filter(email=q)


@ajax_select.register("name")
class NameLookup(ajax_select.LookupChannel):
    def get_query(self, q, request):
        return ["Joseph Simmons", "Darryl McDaniels", "Jam Master Jay"]


@ajax_select.register("author")
class AuthorLookup(ajax_select.LookupChannel):
    model = Author
