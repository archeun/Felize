from django import template

register = template.Library()


@register.inclusion_tag('lib/message_component.html')
def render_message(messages):
    return {'messages': messages}
