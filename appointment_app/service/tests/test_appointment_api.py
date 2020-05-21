import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import AppointmentScheduling, Pediatrician, Appointment
from service.serializers import AppointmentSchedulingSerializer, AppointmentSerializer
from django.utils import timezone

APPOINTMENTS_URL = reverse("service:appointment-list")


def detail_url(appointment_id):
    """Return appointment detail URL"""
    return reverse("service:appointment-detail", args=[appointment_id])


class PrivateAppointmentTests(TestCase):
    """Test authenticated Appointmen API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("alfonso@test.com", "testpass")
        self.pediatrician = Pediatrician.objects.create(name="Test P")
        self.appointment_scheduling = AppointmentScheduling.objects.create(
            pediatrician=self.pediatrician,
            time_start=timezone.now() - datetime.timedelta(hours=1),
            time_finish=timezone.now(),
        )
        self.client.force_authenticate(self.user)

    def test_create_basic_appointment(self):
        """Test creating appointment scheduling"""
        payload = {
            "user": self.user.id,
            "appointment_scheduling": self.appointment_scheduling.id,
            "comments": "One comments",
        }
        res = self.client.post(APPOINTMENTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_basic_appointment_not_available(self):
        """Test creating appointment scheduling not available"""

        app_scheduling = AppointmentScheduling.objects.create(
            pediatrician=self.pediatrician,
            time_start=timezone.now() - datetime.timedelta(hours=1),
            time_finish=timezone.now(),
            is_available=False,
        )
        payload = {
            "user": self.user.id,
            "appointment_scheduling": app_scheduling.id,
            "comments": "One comments",
        }
        res = self.client.post(APPOINTMENTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_appointment_list(self):
        """Test retrieving list of appointment"""
        Appointment.objects.create(
            user=self.user,
            appointment_scheduling=self.appointment_scheduling,
            comments="comments",
        )
        Appointment.objects.create(
            user=self.user,
            appointment_scheduling=self.appointment_scheduling,
            comments="comments",
        )

        res = self.client.get(APPOINTMENTS_URL)

        appointment = Appointment.objects.all().order_by("-id")
        serializer = AppointmentSerializer(appointment, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_appointment_limited_to_user(self):
        """Test that only appointments for authenticated user are returned"""
        user2 = get_user_model().objects.create_user("other@gmail.com", "testpass")
        Appointment.objects.create(
            user=user2,
            appointment_scheduling=self.appointment_scheduling,
            comments="comments",
        )

        appointment = Appointment.objects.create(
            user=self.user,
            appointment_scheduling=self.appointment_scheduling,
            comments="comments",
        )

        res = self.client.get(APPOINTMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["user"], appointment.user.id)

    def test_partial_update_appointment(self):
        """Test updating a appointment with patch"""
        appointment = Appointment.objects.create(
            user=self.user,
            appointment_scheduling=self.appointment_scheduling,
            comments="comments",
        )
        appointment_scheduling = AppointmentScheduling.objects.create(
            pediatrician=self.pediatrician,
            time_start=timezone.now() - datetime.timedelta(hours=1),
            time_finish=timezone.now(),
        )
        payload = {
            "comments": "Chaged",
            "appointment_scheduling": appointment_scheduling.id,
        }
        url = detail_url(appointment.id)
        self.client.patch(url, payload)
        appointment.refresh_from_db()
        self.assertEqual(appointment.comments, payload["comments"])

    def test_full_update_appointment(self):
        """Test updating a appointment with patch"""
        appointment = Appointment.objects.create(
            user=self.user,
            appointment_scheduling=self.appointment_scheduling,
            comments="comments",
        )
        appointment_scheduling = AppointmentScheduling.objects.create(
            pediatrician=self.pediatrician,
            time_start=timezone.now() - datetime.timedelta(hours=1),
            time_finish=timezone.now(),
        )
        new_user = get_user_model().objects.create_user("other@gmail.com", "testpass")
        payload = {
            "comments": "Chaged again",
            "appointment_scheduling": appointment_scheduling.id,
            "user": new_user.id,
        }
        url = detail_url(appointment.id)
        self.client.put(url, payload)
        appointment.refresh_from_db()
        self.assertEqual(appointment.comments, payload["comments"])

    def test_create_bad_request_appointment(self):
        """Test creating appointment"""
        payload = {
            "user": "",
            "appointment_scheduling": "",
            "comments": "",
        }
        res = self.client.post(APPOINTMENTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
