from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ungettext_lazy

import ast
import string


class MaxChoicesValidator(validators.BaseValidator):
    message = ungettext_lazy(
        'Ensure this value has at most %(limit_value)d choice (it has %(show_value)d).',  # NOQA
        'Ensure this value has at most %(limit_value)d choices (it has %(show_value)d).',  # NOQA
        'limit_value'
    )
    code = 'max_choices'

    def compare(self, a, b):
        return a > b

    def clean(self, x):
        lst = ast.literal_eval(x)
        return len(lst)


class MinChoicesValidator(validators.BaseValidator):
    message = ungettext_lazy(
        'Ensure this value has at least %(limit_value)d choice (it has %(show_value)d).',
        'Ensure this value has at least %(limit_value)d choices (it has %(show_value)d).',
        'limit_value'
    )
    code = 'min_choices'

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        lst = ast.literal_eval(x)
        return len(lst)


class EverythingCheckedValidator(validators.BaseValidator):
    message = ungettext_lazy(
        'Ensure that you checked the choice.',
        'Ensure that you checked all the choices.',
    )
    code = 'everything_checked'

    def compare(self, a, b):
        return a != b

    def clean(self, x):
        lst = ast.literal_eval(x)
        return len(lst)


def none_validator(x):
    x = ast.literal_eval(x)
    if 'none' in x and len(x) > 1:
        raise ValidationError('You cannot choose both "None" and another option.')


# 2017-06-20`07:14:39 -- adapted from Connect OER's "twitter_handle_validator"
def twitter_username_validator(value):
    if len(value) == 0:
        raise ValidationError('Twitter username cannot cannot be empty.')

    if value[0] != '@':
        raise ValidationError('Twitter username must start with @.')

    if '@' in value[1:]:
        raise ValidationError('Twitter username can only contain @ as the *first* character.')

    if set(value) - set(string.ascii_letters + string.digits + '_' + '@'):
        raise ValidationError('Invalid character(s) in the Twitter username.')


# 2017-06-20`11:19:15 -- custom ORCID validator
def orcid_validator(value):
    pass

    value = value.upper()

    if set(value) - set(string.digits + '-' + 'X'):
        raise ValidationError('ORCID can only contain digits, hyphens, and the letter "X".')

    if "X" in value[:-1]:
        raise ValidationError('The letter "X" is only acceptable as the final checksum character in ORCID.')

    if value[-1:] not in (string.digits + "X"):
        raise ValidationError("""ORCID's final checksum character can be either a digit or the letter "X".""")

    value = ''.join(c for c in value if (c.isdigit() or c == "X"))
    # value = value.replace('-', '')

    if len(value) != 16:
        raise ValidationError('ORCID must contain exactly 16 digits.')

# 2017-06-24`00:20:27 -- custom expenses validator
def expenses_validator(x):
    x = ast.literal_eval(x)
    if 'fee_full' in x and 'fee_discount' in x:
        raise ValidationError('Full conference fee and 50% discount on conference registration fee cannot both be checked.')
