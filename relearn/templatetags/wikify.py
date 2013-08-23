# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='dewikify')
@stringfilter
def dewikify(name):
    name = name.replace('-', ' ')
    name = name.replace('::', u' → ')
    return name
