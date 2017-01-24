# - coding: utf-8  -
from django import template

register = template.Library()


@register.inclusion_tag('custom_tags/messaging.html')
def messaging(user, *args, **kwargs):
    return {'user': user}
