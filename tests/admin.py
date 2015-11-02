
from django.contrib import admin
from tests.models import Author


class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Author, AuthorAdmin)
