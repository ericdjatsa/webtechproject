#!/usr/bin/env python

from django.core.management import setup_environ
import settings
from src.crawler.models import *
from src.crawler.utils import *

#from src.frontend.models import Film

setup_environ(settings)
crawler = Crawler()
crawler.crawl()

File.objects.all().delete()

#just for demo
#Film.objects.all().delete()

crawler.saveToDB()

