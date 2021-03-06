from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.models import AppointmentScheduling, Appointment, Pediatrician
from rest_framework.exceptions import ValidationError


class UserSerializers(serializers.ModelSerializer):
    """Serializers for the users object"""

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validate_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validate_data)


class AuthTokenSerializers(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            message = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(message, code="authentication")

        attrs["user"] = user

        return attrs


class PediatricianSerializer(serializers.ModelSerializer):
    """Serialize Pediatrician"""

    class Meta:
        model = Pediatrician
        fields = (
            "id",
            "name",
            "genre",
        )
        read_only_fields = ("id",)


class AppointmentSchedulingSerializer(serializers.ModelSerializer):
    """Serialize AppointmentScheduling"""

    pediatrician_data = serializers.SerializerMethodField()

    @staticmethod
    def get_pediatrician_data(obj):
        serializers = PediatricianSerializer(obj.pediatrician)
        return serializers.data

    class Meta:
        model = AppointmentScheduling
        fields = (
            "id",
            "pediatrician",
            "time_start",
            "time_finish",
            "is_available",
            "pediatrician_data",
        )
        read_only_fields = ("id",)


class AppointmentSerializer(serializers.ModelSerializer):
    """Serialize Appointment"""

    appointment_scheduling_data = serializers.SerializerMethodField()

    @staticmethod
    def get_appointment_scheduling_data(obj):
        serializers = AppointmentSchedulingSerializer(obj.appointment_scheduling)
        return serializers.data

    def validate(self, data):
        if data.get("appointment_scheduling"):
            appointment_scheduling = data.get("appointment_scheduling")
            search = AppointmentScheduling.objects.get(pk=appointment_scheduling.id)
            if not search.is_available:
                msg = "not available"
                raise ValidationError(msg)
        return data

    class Meta:
        model = Appointment
        fields = (
            "id",
            "user",
            "appointment_scheduling",
            "comments",
            "appointment_scheduling_data",
        )
        read_only_fields = ("id",)
