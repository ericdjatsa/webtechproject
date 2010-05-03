from django import template
import playground.utils.trailer_addict

register = template.Library()
@register.filter("key")
def key(h, key):
	try:
		return h[key]
	except:
		return u''

@register.filter("trailer_addict_embedded_player")
def trailer_addict_embedded_player(film, playerSize):
	return playground.utils.trailer_addict.getTrailerAddictEmbeddedPlayer(film, playerSize)
