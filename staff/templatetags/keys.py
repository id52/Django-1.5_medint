from django import template

register = template.Library()


@register.inclusion_tag('custom_tags/keys.html')
def keys(user, *args, **kwargs):
    return {'user': user}
