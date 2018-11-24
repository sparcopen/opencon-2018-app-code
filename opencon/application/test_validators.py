from .validators import MaxChoicesValidator, MinChoicesValidator, EverythingCheckedValidator
from django.test import SimpleTestCase
from django.core.validators import ValidationError


class FormValidatorsTest(SimpleTestCase):
    def test_max_choice(self):
        validator = MaxChoicesValidator(2)

        self.assertIsNone(validator('[0]'))
        self.assertIsNone(validator('[0, 1]'))

        with self.assertRaises(ValidationError):
            validator('[0, 1, 2]')

    def test_min_choice(self):
        validator = MinChoicesValidator(2)

        self.assertIsNone(validator('[0, 1]'))
        self.assertIsNone(validator('[0, 1, 2]'))

        with self.assertRaises(ValidationError):
            validator('[0]')

    def test_every_choice(self):
        validator = EverythingCheckedValidator(2)

        self.assertIsNone(validator('[0, 1]'))

        with self.assertRaises(ValidationError):
            validator('[0]')

        with self.assertRaises(ValidationError):
            validator('[0, 1, 2]')
