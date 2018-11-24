from .validators import rating_validator, ValidationError
from django.test import SimpleTestCase


class TestRatingValidator(SimpleTestCase):
    def test_rating_validator_high(self):
        with self.assertRaises(ValidationError):
            rating_validator(11)

        with self.assertRaises(ValidationError):
            rating_validator(10.1)

    def test_rating_validator_negative(self):
        with self.assertRaises(ValidationError):
            rating_validator(-0.1)

    def test_rating_validator_valid(self):
        self.assertIsNone(rating_validator(0))
        self.assertIsNone(rating_validator(7.3))
        self.assertIsNone(rating_validator(10))
