from django import template
from src.utils.trailer_addict import getTrailerAddictEmbeddedPlayer

register = template.Library()
@register.filter("key")
def key(h, key):
	try:
		return h[key]
	except:
		return u''

@register.filter("trailer_addict_embedded_player")
def trailer_addict_embedded_player(film, playerSize):
	return getTrailerAddictEmbeddedPlayer(film, playerSize)
