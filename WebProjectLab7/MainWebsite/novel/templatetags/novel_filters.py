from django import template

register = template.Library()


@register.filter
def ru_plural(value, arg):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    words = arg.split(',')
    if value % 10 == 1 and value % 100 != 11:
        return f"{value} {words[0]}"
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return f"{value} {words[1]}"
    else:
        return f"{value} {words[2]}"