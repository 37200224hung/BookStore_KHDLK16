from django import template

register = template.Library()

@register.filter
def intmul(value, arg):
    return int(value) * int(arg)
