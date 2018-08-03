from django import template

register = template.Library()


@register.filter('inputtype')
def inputtype(ob):
    return ob.__class__.__name__
