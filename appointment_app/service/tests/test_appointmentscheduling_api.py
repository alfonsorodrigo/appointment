import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import AppointmentScheduling, Pediatrician
from service.serializers import AppointmentSchedulingSerializer
from django.utils import timezone
import json

APPOINTMENTSCHEDULE_URL = reverse("service:appointmentscheduling-list")


def sample_appointmentscheduling(pediatrician, **params):
    """Create and return a sample appointmentscheduling"""
    defaults = {
        "time_start": timezone.now() - datetime.timedelta(hours=1),
        "time_finish": timezone.now(),
    }
    defaults.update(params)

    return AppointmentScheduling.objects.create(pediatrician=pediatrician, **defaults)


class PublicAppointmentSchedulingApiTests(TestCase):
    """Test unauthenticated AppointmentScheduling API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(APPOINTMENTSCHEDULE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAppointmentSchedulingApiTests(TestCase):
    """Test authenticated AppointmentScheduling API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("alfonso@test.com", "testpass")
        self.client.force_authenticate(self.user)
        self.pediatrician = Pediatrician.objects.create(name="Edgar Vazquez")

    def test_retrieve_appointment_scheduling(self):
        """Test retrieving list of appointment_scheduling"""
        sample_appointmentscheduling(pediatrician=self.pediatrician)
        sample_appointmentscheduling(pediatrician=self.pediatrician)

        res = self.client.get(APPOINTMENTSCHEDULE_URL)

        appointment_scheduling = AppointmentScheduling.objects.all().order_by("-id")
        serializer = AppointmentSchedulingSerializer(appointment_scheduling, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_appointment_scheduling(self):
        """Test creating appointment scheduling"""
        payload = {
            "pediatrician": self.pediatrician.id,
            "time_start": timezone.now() - datetime.timedelta(hours=1),
            "time_finish": timezone.now(),
        }
        res = self.client.post(APPOINTMENTSCHEDULE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_bad_request_appointment_scheduling(self):
        """Test creating appointment scheduling"""
        payload = {
            "pediatrician": "",
            "time_start": "",
            "time_finish": "",
        }
        res = self.client.post(APPOINTMENTSCHEDULE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
