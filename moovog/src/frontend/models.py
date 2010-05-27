# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.db import IntegrityError

# Create your models here.
# Contains the data model of a message

class Genre(models.Model):
	name = models.CharField(max_length=20, unique = True)
	def __unicode__(self):
		return self.name
	def save(self):
		if Genre.objects.filter(name = self.name).__len__() == 0:
			super(Genre, self).save()

class Person(models.Model):
	name = models.CharField(max_length=50)
	birth_name = models.CharField(max_length=50, null = True)
	birth_date = models.DateField(null = True)
	death_date = models.DateField(null = True)
	imdb_id = models.CharField(max_length = 14, unique = True)
	bio = models.TextField(null = True)
	is_full = models.BooleanField()
	image_url = models.CharField(max_length=256, null = True)
	def __unicode__(self):
		return self.name
	def save(self):
		if Person.objects.filter(imdb_id = self.imdb_id).__len__() == 0:
			super(Person, self).save()
		elif self.is_full:
			#perform update
			self._set_pk_val(Person.objects.get(imdb_id = self.imdb_id).pk)
			super(Person, self).save()
			
class Character(models.Model):
	name = models.CharField(max_length=50)
	imdb_id = models.CharField(max_length = 14, null = True)
	is_full = models.BooleanField()
	def __unicode__(self):
		return self.name
	def save(self):
		if Character.objects.filter(imdb_id = self.imdb_id).filter(name = self.name).__len__() == 0:
			super(Character, self).save()
#		elif Character.objects.filter(imdb_id = self.imdb_id).filter(is_full = True).__len__() == 0 or self.is_full:
#			super(Character, self).update()
	

class Movie(models.Model):
	title = models.CharField(max_length=100)
	year = models.CharField(max_length=10)
	image_url = models.CharField(max_length=255)
	filename = models.CharField(max_length = 256)
	extension = models.CharField(max_length = 32)
	path = models.CharField(max_length = 256)
	hash_code = models.CharField(max_length = 72)
	imdb_id = models.CharField(max_length = 14, unique = True)
	plot = models.TextField()
	short_plot = models.TextField()
	genres = models.ManyToManyField(Genre)	
	is_full = models.BooleanField()
	runtimes = models.CharField(max_length = 64)
	rating = models.FloatField()
	def __unicode__(self):
		return "%s (%s)" % (self.title, self.year)

class ActedIn(models.Model):
	actor = models.ForeignKey(Person)
	character = models.ForeignKey(Character)
	movie = models.ForeignKey(Movie)
	def __unicode__(self):
		u"%s played %s in %s" % (self.actor, self.character, self.movie)
	def save(self):
		if ActedIn.objects.filter(actor = self.actor).filter(character = self.character).filter(movie = self.movie).__len__() == 0:
			try:
				super(ActedIn, self).save()
			except IntegrityError, e:
				print "ActedIn has inconsistent data: %s" % (self.__unicode__())

class Directed(models.Model):
	person = models.ForeignKey(Person)
	movie = models.ForeignKey(Movie)
	def __unicode__(self):
		return "%s directed %s" % (self.person, self.movie)
	def save(self):
		if Directed.objects.filter(person = self.person).filter(movie = self.movie).__len__() == 0:
			super(Directed, self).save()
		
class Wrote(models.Model):
	person = models.ForeignKey(Person)
	movie = models.ForeignKey(Movie)
	def __unicode__(self):
		return "%s wrote %s" % (self.person, self.movie)
	def save(self):
		if Wrote.objects.filter(person = self.person).filter(movie = self.movie).__len__() == 0:
			super(Wrote, self).save()

class IgnoreTable(models.Model):
	filename = models.CharField(max_length=256)
	extension = models.CharField(max_length=32)
	path = models.CharField(max_length=256)
	hash_code = models.CharField(max_length=72)
	def __unicode__(self):
		return self.path

class ImdbCache(models.Model):
	imdb_id = models.CharField(max_length=12, primary_key = True)
	is_full = models.BooleanField()
	content = models.TextField()
	def __unicode__(self):
		return self.imdb_id

class ImdbSearch(models.Model):
	keyword = models.CharField(max_length = 256)
	result_index = models.IntegerField()
	imdb_obj = models.ForeignKey(ImdbCache)
	def __unicode__(self):
		return "%s (%d): %s" % (self.keyword, self.result_index, self.imdb_obj)
	
class Trailer(models.Model):
	imdb_id = models.CharField(max_length=12, unique=True)
	trailer_url = models.CharField(max_length = 256)
	def __unicode__(self):
		return self.imdb_id
		
def get_or_create_person(name, imdb_id):
	p = Person.objects.filter(name = name).filter(imdb_id = imdb_id)
	if p.__len__() > 0:
		return p[0]
	else:
		p = Person(name = name, imdb_id = imdb_id, is_full = False)
		p.save()
	return p
	
def get_or_create_character(name, imdb_id = None):
	c = Character.objects.filter(name = name)
	if imdb_id != None:
		c = c.filter(imdb_id = imdb_id)
	if c.__len__() > 0:
		return c[0]
	else:
		c = Character(name = name, imdb_id = imdb_id, is_full = False)
		c.save()
	return c
	
def get_or_create_genre(name):
	g = Genre.objects.filter(name = name)
	if g.__len__() == 0:
		g = Genre(name = name)
		g.save()
		return g
	else:
		return g[0]
