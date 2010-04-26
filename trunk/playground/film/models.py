from django.db import models
from datetime import datetime

# Create your models here.
# Contains the data model of a message
class Film(models.Model):
	title = models.CharField(max_length=30)
	release_date = models.DateTimeField('release_date')
	image = models.CharField(max_length=200)

