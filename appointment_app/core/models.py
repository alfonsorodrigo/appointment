from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


def get_hour_appointment(date):
    return timezone.localtime(date).strftime("%H:%M %p")


def get_date_appointment(date):
    return timezone.localtime(date).strftime("%Y-%m-%d")


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model than suppor using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


GENRE = (
    ("M", "Masculino"),
    ("F", "Femenino"),
)


class AuditTrail(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Pediatrician(AuditTrail):
    name = models.CharField(max_length=250, blank=True)
    genre = models.CharField(max_length=1, choices=GENRE, default="M")

    class Meta:
        verbose_name = "Pediatra"
        verbose_name_plural = "Pediatras"
        ordering = ["-created"]

    def __str__(self):
        return self.name


class AppointmentScheduling(AuditTrail):
    pediatrician = models.ForeignKey(Pediatrician, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_finish = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Programación de cita"
        verbose_name_plural = "Programación de citas"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.pediatrician.name} el {get_date_appointment(self.time_start)}  de {get_hour_appointment(self.time_start)} a {get_hour_appointment(self.time_finish)}"


class Appointment(AuditTrail):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment_scheduling = models.ForeignKey(
        AppointmentScheduling, on_delete=models.CASCADE
    )
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ["-created"]

    def __str__(self):
        return self.user.email
