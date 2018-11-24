from .helpers import is_valid_email_address
from django.test import SimpleTestCase


class EmailValidatorTest(SimpleTestCase):
    def test_invalid_email(self):
        self.assertFalse(is_valid_email_address(''))
        self.assertFalse(is_valid_email_address('no@mail'))

    def test_valid_email(self):
        self.assertTrue(is_valid_email_address('valid@email.com'))
