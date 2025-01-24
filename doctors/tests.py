from django.test import TestCase
from django.urls import reverse
from .models import Doctor, Specialization

class DoctorTests(TestCase):
    def setUp(self):
        self.specialization = Specialization.objects.create(
            name="Orthodontist"
        )
        self.doctor = Doctor.objects.create(
            name="Dr. Test",
            email="doctor@test.com",
            phone="1234567890",
            specialization=self.specialization
        )

    def test_doctor_list(self):
        response = self.client.get(reverse('doctors:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor.name)

    def test_doctor_detail(self):
        response = self.client.get(
            reverse('doctors:detail', kwargs={'pk': self.doctor.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor.specialization.name)
