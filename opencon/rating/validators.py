from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def rating_validator(value):
    if not(0 <= value <= 10):
        raise ValidationError(
            _('%(value)s is not in range <0, 10>'),
            params={'value': value},
        )
