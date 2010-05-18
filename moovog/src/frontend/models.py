# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

# Create your models here.
# Contains the data model of a message
class Film(models.Model):
	title = models.CharField(max_length=30)
	year = models.CharField(max_length=4)
	image = models.CharField(max_length=200)
	filename = models.CharField(max_length = 256)
	extension = models.CharField(max_length = 32)
	path = models.CharField(max_length = 256)
	hash_code = models.CharField(max_length = 64)
	imdb_id = models.CharField(max_length = 12)

class IgnoreTable(models.Model):
	filename = models.CharField(max_length=256)
	extension = models.CharField(max_length=32)
	path = models.CharField(max_length=256)
	md5 = models.CharField(max_length=64)

class ImdbCache(models.Model):
	imdb_id = models.CharField(max_length=12)
	keyword = models.CharField(max_length=256)
	result_index = models.IntegerField()
	content = models.TextField()
	
class Trailer(models.Model):
	imdb_id = models.CharField(max_length=12)
	trailer_url = models.CharField(max_length = 256)
	
