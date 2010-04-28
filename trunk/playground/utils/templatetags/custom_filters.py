from django import template


register = template.Library()
@register.filter("key")
def key(h, key):
	try:
		return h[key]
	except:
		return u''
