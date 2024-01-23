from django import template

register = template.Library()

@register.filter
def page_range(value, args):
    print(value, args)
    start, end = map(int, args.split(','))
    return list(range(max(start, 1), min(end, value) + 1))