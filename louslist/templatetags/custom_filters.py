from django import template

register = template.Library()

def is_numeric(value):
    return value.isdigit()
register.filter('is_numeric', is_numeric)