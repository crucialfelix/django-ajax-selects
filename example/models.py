# -*- coding: utf8 -*-

from django.db import models


class Person(models.Model):

    """ an actual singular human being """
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Group(models.Model):

    """ a music group """

    name = models.CharField(max_length=200,unique=True)
    members = models.ManyToManyField(Person,blank=True,help_text="Enter text to search for and add each member of the group.")
    url = models.URLField(blank=True)

    def __unicode__(self):
        return self.name


class Label(models.Model):

    """ a record label """

    name = models.CharField(max_length=200,unique=True)
    owner = models.ForeignKey(Person,blank=True,null=True)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return self.name


class Song(models.Model):

    """ a song """

    title = models.CharField(blank=False, max_length=200)
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return self.title


class Release(models.Model):

    """ a music release/product """

    title = models.CharField(max_length=100)
    catalog = models.CharField(blank=True, max_length=100)

    group = models.ForeignKey(Group,blank=True,null=True,verbose_name=u"Русский текст")
    label = models.ForeignKey(Label,blank=False,null=False)
    songs = models.ManyToManyField(Song,blank=True)

    def __unicode__(self):
        return self.title



class Author(models.Model):
   name = models.CharField(max_length=100)

class Book(models.Model):
   author = models.ForeignKey(Author)
   title = models.CharField(max_length=100)
   about_group = models.ForeignKey(Group)
   mentions_persons = models.ManyToManyField(Person)

