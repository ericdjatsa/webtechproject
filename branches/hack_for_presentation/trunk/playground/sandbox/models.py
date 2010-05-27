from django.db import models
from datetime import datetime

# Create your models here.
# Contains the data model of a message
class Message(models.Model):
	title = models.CharField(max_length=30)
	text = models.CharField(max_length=200)
	timestamp = models.DateTimeField('Timestamp')

	def save(self):
		# on save, update the message timestamp
		self.timestamp = datetime.now()
		super(Message, self).save()

