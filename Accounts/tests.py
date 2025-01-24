from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User,Profile

class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        response = self.client.post(reverse('Accounts:register'), self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

    def test_user_login(self):
        get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        response = self.client.post(reverse('Accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_profile_creation(self):
        user = get_user_model().objects.create_user(**self.user_data)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('Accounts:profile_update'), {
            'phone_number': '1234567890',
            'address': 'Test Address'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user=user).exists())
