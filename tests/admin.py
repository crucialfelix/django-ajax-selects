
from django.contrib import admin
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminTabularInline, AjaxSelectAdminStackedInline
from tests.models import Author, Book, Person
from tests.test_integration import BookForm
from tests import lookups2  # noqa


class BookAdmin(AjaxSelectAdmin):
    form = BookForm
admin.site.register(Book, BookAdmin)


class BookInline(AjaxSelectAdminTabularInline):

    model = Book
    form = BookForm
    extra = 2


class AuthorAdmin(AjaxSelectAdmin):

    inlines = [
        BookInline
    ]

admin.site.register(Author, AuthorAdmin)


class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person, PersonAdmin)
