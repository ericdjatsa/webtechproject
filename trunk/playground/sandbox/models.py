from django.db import models

# Create your models here.
class Message(models.Model):
	title = models.CharField(max_length=30)
	text = models.CharField(max_length=200)
	timestamp = models.DateTimeField('Timestamp')

