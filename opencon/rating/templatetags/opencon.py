from django import template


register = template.Library()


@register.assignment_tag
def i_rated(ratings, application):
    for rating in ratings:
        if rating.application == application:
            return True
    return False
