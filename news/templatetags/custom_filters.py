from django import template

register = template.Library()

@register.filter (name = 'Censor')
def Censor (value):
    cens = ('qwerty', 'solomid')
    text = set(value.split())
    for x in text:
        for y in cens:
            if x == y:
                return value.replace(x, '-',3)
    return value

