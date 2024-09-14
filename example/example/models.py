from django.db import models


class Person(models.Model):
    """an actual singular human being."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Group(models.Model):
    """a music group."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, help_text="Name of the group")
    members = models.ManyToManyField(
        Person,
        blank=True,
        help_text="Enter text to search for and add each member of the group.",
    )
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    """a record label."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    owner = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    """a song."""

    id = models.AutoField(primary_key=True)
    title = models.CharField(blank=False, max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Release(models.Model):
    """a music release/product."""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    catalog = models.CharField(blank=True, max_length=100)

    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        verbose_name="Русский текст (group)",
        on_delete=models.CASCADE,
    )
    label = models.ForeignKey(Label, blank=False, null=False, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, blank=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    """
    Author has multiple books, via foreign keys.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Book has no admin, its an inline in the Author admin."""

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    about_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    mentions_persons = models.ManyToManyField(Person, help_text="Person lookup renders html in menu")

    def __str__(self):
        return self.title
