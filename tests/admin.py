from django.contrib import admin

from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminTabularInline
from tests.models import Author, Book, Person
from tests.test_integration import BookForm


@admin.register(Book)
class BookAdmin(AjaxSelectAdmin):
    form = BookForm


class BookInline(AjaxSelectAdminTabularInline):
    model = Book
    form = BookForm
    extra = 2


@admin.register(Author)
class AuthorAdmin(AjaxSelectAdmin):
    inlines = [
        BookInline
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
