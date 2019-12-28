from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        app_label = 'tests'


class PersonWithTitle(Person):
    """
    Testing an inherited model (multi-table)
    """

    title = models.CharField(max_length=150)

    class Meta:
        app_label = 'tests'


class Author(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'tests'


class Book(models.Model):
    """ Book has no admin, its an inline in the Author admin"""

    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    mentions_persons = models.ManyToManyField(Person, help_text="MENTIONS PERSONS HELP TEXT")

    class Meta:
        app_label = 'tests'
