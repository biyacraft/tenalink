from django import template

register = template.Library()


@register.tag
def sum_all(objects, colm):
    return sum(getattr(obj, colm) for obj in objects)
