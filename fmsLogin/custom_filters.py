from urllib.parse import quote
from django import template

register = template.Library()

@register.filter
def url_encode(value):
    return quote(value)

