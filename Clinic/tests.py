from django.test import TestCase
from django.urls import reverse
from .models import Clinic, Service

class ClinicTests(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(
            name="Junction Dental",
            address="123 Test St",
            phone="1234567890",
            email="clinic@test.com"
        )
        self.service = Service.objects.create(
            name="Cleaning",
            description="Dental Cleaning",
            price=1000.00
        )

    def test_clinic_details(self):
        response = self.client.get(reverse('clinic:detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.clinic.name)

    def test_services_list(self):
        response = self.client.get(reverse('clinic:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service.name)
