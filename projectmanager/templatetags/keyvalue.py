from django import template

register = template.Library()


@register.filter('keyvalue')
def keyvalue(dict, key):
    if key in dict:
        return dict[key]
    return ''
