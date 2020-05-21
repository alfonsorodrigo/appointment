from rest_framework import generics
from .serializers import UserSerializers, AuthTokenSerializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from core.models import AppointmentScheduling, Appointment
from rest_framework.authentication import TokenAuthentication
from .serializers import AppointmentSchedulingSerializer, AppointmentSerializer


class ModelViewSet(viewsets.ModelViewSet):
    """ Enable the default Django model permission backend"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializers
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class AppointmentSchedulingViewSet(ModelViewSet):
    """Manage Appointment Scheduling in the database"""

    queryset = AppointmentScheduling.objects.all()
    serializer_class = AppointmentSchedulingSerializer


class AppointmentViewSet(ModelViewSet):
    """Manage Appointment in the database"""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-id")
