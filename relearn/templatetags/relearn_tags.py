import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def natural_join(val, cjn="and"):
    """
    Gracefully joins a list of things.

    >>> natural_join(['pierre'])
    'pierre'

    >>> natural_join(['pierre', 'paul'])
    'pierre and paul'

    >>> natural_join(['pierre', 'paul', 'jacques'])
    'pierre, paul and jacques'

    >>> natural_join(['pierre', 'paul', 'jacques'], cnj="et")
    'pierre, paul et jacques'
    """
    
    def to_string(object):
        if isinstance(object, str) or isinstance(object, unicode):
            return object
        try:
            return object.__unicode__()
        except AttributeError:
            return repr(object)
        
    val = [to_string(object) for object in val]
    return " ".join((", ".join(val[0:-1]), "%s %s" % (cjn, val[-1]))) if len(val) > 1 else val[0]



@register.filter(is_safe=True)
@stringfilter
def markdown_filter(value):
    extensions = ["extra", ]

    return mark_safe(markdown.markdown(force_unicode(value),
                                       extensions))
