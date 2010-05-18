from django import template
from src.utils.trailer_addict import getTrailerAddictEmbeddedPlayer
from src.utils.internet_movie_archive import get_trailer_embed
from src.utils.get_image import getOrCacheImage

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

@register.filter("trailer_addict_embedded_player")
def trailer_addict_embedded_player(film, playerSize):
	return getTrailerAddictEmbeddedPlayer(film, playerSize)

@register.filter("internet_movie_archive_player")
def internet_movie_archive_player(imdb_id):
	print "IMDB id: %s" % (imdb_id)
	return get_trailer_embed(u"tt%s" % (imdb_id))

@register.filter("get_cover_image")
def get_cover_image(imdb_url):
	return getOrCacheImage(imdb_url)
