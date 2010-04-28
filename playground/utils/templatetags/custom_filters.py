from django import template


register = template.Library()
@register.filter("key")
def key(h, key):
    return h[key]
