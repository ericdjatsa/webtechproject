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
	name = models.CharField(max_length=32)
	birth_name = models.CharField(max_length=32, null = True)
	birth_date = models.DateField(null = True)
	death_date = models.DateField(null = True)
	imdb_id = models.CharField(max_length = 12, unique = True)
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
			self.set_pk_val(Person.objects.filter(imdb_id = self.imdb_id)[0].pk)
			super(Person, self).save()
	def fetch(self):
		if (not self.is_full) and (self.imdb_id != None):
			i = imdbUpdate(imdbGetPerson(self.imdb_id))
			try: self.birth_date = datetime.strptime(i['birth date'], "%d %B %Y").date()
			except: self.birth_date = None
			try: self.death_date = datetime.strptime(i['death date'], "%d %B %Y").date()
			except: self.death_date = None
			try: self.image_url = i['headshot']
			except: self.image_url = None
			try: self.bio = i['mini biography']
			except: self.bio = None
			try: self.birth_name = i['birth name']
			except: self.birth_name = None
			self.save()
			
class Character(models.Model):
	name = models.CharField(max_length=32)
	imdb_id = models.CharField(max_length = 12, null = True)
	is_full = models.BooleanField()
	def __unicode__(self):
		return self.name
	def save(self):
		if Character.objects.filter(imdb_id = self.imdb_id).filter(name = self.name).__len__() == 0:
			super(Character, self).save()
#		elif Character.objects.filter(imdb_id = self.imdb_id).filter(is_full = True).__len__() == 0 or self.is_full:
#			super(Character, self).update()
	

class Movie(models.Model):
	title = models.CharField(max_length=30)
	year = models.CharField(max_length=4)
	image_url = models.CharField(max_length=200)
	filename = models.CharField(max_length = 256)
	extension = models.CharField(max_length = 32)
	path = models.CharField(max_length = 256)
	hash_code = models.CharField(max_length = 64)
	imdb_id = models.CharField(max_length = 12, unique = True)
	synopsis = models.TextField()
	plot = models.TextField()
	genres = models.ManyToManyField(Genre)	
	is_full = models.BooleanField()
	runtimes = models.IntegerField()
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
	hash_code = models.CharField(max_length=64)
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
