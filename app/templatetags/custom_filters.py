from django import template

register = template.Library()

@register.filter
def custom_price(value):
    try:
        return "{:,}".format(int(value))
    except:
        return value