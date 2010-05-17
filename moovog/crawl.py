#!/usr/bin/env python

from django.core.management import setup_environ
import settings
from src.crawler.models import *
from src.crawler.utils import *

setup_environ(settings)
crawler = Crawler()
crawler.crawl()
File.objects.all().delete()
crawler.saveToDB()

