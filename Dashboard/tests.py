from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create staff user
        self.staff_user = get_user_model().objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )

    def test_dashboard_login_required(self):
        """Test dashboard is not accessible without login"""
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_dashboard_with_login(self):
        """Test dashboard is accessible after login"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_staff_access(self):
        """Test staff-only sections are properly restricted"""
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('dashboard:staff'))
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        """Test dashboard context contains required data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertTrue('appointments' in response.context)
        self.assertTrue('recent_activity' in response.context)

    def test_unauthorized_staff_access(self):
        """Test non-staff users cannot access staff areas"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:staff'))
        self.assertEqual(response.status_code, 403)
