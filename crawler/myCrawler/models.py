#Application:myCrawler
from django.db import models
from django.contrib import admin
try:
	#for python 2.6
	import hashlib
	md5_constructor = hashlib.md5()
except ImportError:
	#for python 2.5
	import md5
	md5_constructor = md5.new()

class File(models.Model):
	filename = models.CharField(max_length=255)
	extension = models.CharField(max_length=5)
	path = models.CharField(max_length=300)
	hash_code = models.CharField(max_length=300)

	def __unicode__(self):
		return self.filename
	
	#calcuates a file's url, and md5, also stores path, url, and md5 as attributes
	def setFields(self,path,index):
		self.path=path
		self.index=index
			
	def genMD5(self,depth=None):
		print 'entering genMD5'
		#if not depth:
		#	print 'no value for depth'
		#	f=open(self.path,'rb').read()
		#else:
		print 'file path:',self.path
		f=open(self.path,'rb').read(depth)
		print 'bytes read from file:',f
		#for python 2.5
		#self.hash_code=md5.new(f).hexdigest()
		md5_constructor.update(f)
		self.hash_code=md5_constructor.hexdigest()
		print 'hash code',self.hash_code
		
admin.site.register(File)
