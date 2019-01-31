from django import template

register = template.Library()

@register.filter(name='dictlookup')
def dictlookup(dict, key):    
    return dict[key]