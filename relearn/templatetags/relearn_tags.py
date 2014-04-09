from django import template


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
    if val and isinstance(val, list):
        return " ".join((", ".join(val[0:-1]), "%s %s" % (cjn, val[-1]))) if len(val) > 1 else val[0]
    else:
        return val
