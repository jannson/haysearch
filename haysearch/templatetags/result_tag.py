from django import template
from django.db import models
from haysearch.models import title_beauty
import re

register = template.Library()


@register.filter(name='beauty')
def beauty(value, arg):
    """Removes all values of arg from the given string"""
    if value.strip() == '':
        return title_beauty(arg, 8)
    else:
        return title_beauty(value, 8)

@register.filter(name='beauty2')
def beauty2(value, arg):
    if value.strip() == '':
        return title_beauty(arg, 38)
    else:
        return title_beauty(value, 38)

@register.filter(name='beauty3')
def beauty3(value):
    return title_beauty(value, 10)

@register.filter(name='str_sub')
def str_sub(value, l):
    if len(value) > l:
        return value[0:l]+'......'
    else:
        return value
