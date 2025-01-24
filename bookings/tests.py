from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import Booking
from doctors.models import Doctor

class BookingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testpatient',
            password='testpass123'
        )
        self.doctor = Doctor.objects.create(
            name="Dr. Test",
            email="doctor@test.com"
        )
        self.tomorrow = datetime.now() + timedelta(days=1)

    def test_create_booking(self):
        self.client.login(username='testpatient', password='testpass123')
        response = self.client.post(reverse('bookings:create'), {
            'doctor': self.doctor.id,
            'date': self.tomorrow.date(),
            'time_slot': '10:00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Booking.objects.filter(doctor=self.doctor).exists()
        )

    def test_booking_conflict(self):
        Booking.objects.create(
            patient=self.user,
            doctor=self.doctor,
            date=self.tomorrow.date(),
            time_slot='10:00'
        )
        self.client.login(username='testpatient', password='testpass123')
        response = self.client.post(reverse('bookings:create'), {
            'doctor': self.doctor.id,
            'date': self.tomorrow.date(),
            'time_slot': '10:00'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Booking.objects.filter(
                doctor=self.doctor,
                date=self.tomorrow.date(),
                time_slot='10:00'
            ).count(),
            1
        )
