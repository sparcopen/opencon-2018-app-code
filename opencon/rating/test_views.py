from django.test import TestCase
from .models import User
from django.core.urlresolvers import reverse


class TestLoginView(TestCase):
    def test_valid_user_login(self):
        user = User.objects.create(email='no@mail.com')
        url = reverse('rating:login', kwargs={'uuid': user.uuid.hex})
        redirect_url = reverse('rating:rate_round1')
        response = self.client.get(url)
        self.assertEqual(self.client.session['user_pk'], user.pk)
        self.assertRedirects(response, redirect_url)

    def test_invalid_user_login(self):
        user = User(email='no@mail.com')
        url = reverse('rating:login', kwargs={'uuid': user.uuid.hex})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestLogoutView(TestCase):
    def test_logout_after_login(self):
        user = User.objects.create(email='no@mail.com')
        login_url = reverse('rating:login', kwargs={'uuid': user.uuid.hex})
        login_response = self.client.get(login_url)

        logout_url = reverse('rating:logout')
        logout_response = self.client.get(logout_url)

        self.assertIsNone(self.client.session.get('user_pk'))
