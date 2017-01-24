# - coding: utf-8  -


from django import template

register = template.Library()



@register.inclusion_tag('custom_tags/userinfo.html')
def userinfo(user, *args, **kwargs):
    return {'user': user}

@register.inclusion_tag('custom_tags/patient_list.html')
def patientlist(user, *args, **kwargs):
    return {'user': user}





