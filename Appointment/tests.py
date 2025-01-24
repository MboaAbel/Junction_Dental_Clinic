from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import Appointment

class AppointmentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='testpass123'
        )
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.appointment = Appointment.objects.create(
            patient=self.user,
            appointment_date=self.tomorrow,
            reason='Dental Checkup',
            status='Pending'
        )

    def test_create_appointment(self):
        self.client.login(username='testpatient', password='testpass123')
        response = self.client.post(reverse('appointment:create'), {
            'appointment_date': self.tomorrow,
            'reason': 'Tooth Cleaning',
            'status': 'Pending'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Appointment.objects.filter(reason='Tooth Cleaning').exists())

    def test_appointment_validation(self):
        self.client.login(username='testpatient', password='testpass123')
        past_date = datetime.now() - timedelta(days=1)
        response = self.client.post(reverse('appointment:create'), {
            'appointment_date': past_date,
            'reason': 'Invalid Appointment',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Appointment.objects.filter(reason='Invalid Appointment').exists())
