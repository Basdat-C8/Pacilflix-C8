from django import template

register = template.Library()

@register.filter
def to_range(value):
    return range(value)

@register.simple_tag
def average_rating(reviews):
    if reviews:
        return round(sum([review['rating'] for review in reviews]) / len(reviews), 2)
    else:
        return 0