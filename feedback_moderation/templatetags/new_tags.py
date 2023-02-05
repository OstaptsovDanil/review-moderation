from django import template

register = template.Library()


@register.filter(name='split')
def split(value, splitter):
    return value.split(splitter)


@register.filter(name='is_swear')
def is_swear(word, swearing):
    for swear in swearing:
        if swear.lower() in word.lower():
            return True
    return False
