# -*- coding: utf-8 -*-
from django import template
from src.utils.get_image import getOrCacheImage
from src.frontend.models import Trailer

register = template.Library()
@register.filter("key")
def key(h, key):
	try:
		if key == 'cover url':
			return getOrCacheImage(h[key])
		else:
			return h[key]
	except:
		return u''

@register.filter("internet_movie_archive_player")
def internet_movie_archive_player(imdb_id):
	try:
		return Trailer.objects.filter(imdb_id = imdb_id)[0].trailer_url
	except:
		return u""

@register.filter("get_cover_image")
def get_cover_image(imdb_url):
	return getOrCacheImage(imdb_url)
