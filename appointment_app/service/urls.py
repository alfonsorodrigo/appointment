from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CreateUserView,
    CreateTokenView,
    AppointmentSchedulingViewSet,
    AppointmentViewSet,
)

app_name = "service"

router = DefaultRouter()
router.register("appointmentscheduling", AppointmentSchedulingViewSet)
router.register("appointment", AppointmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("user/create/", CreateUserView.as_view(), name="create"),
    path("user/token/", CreateTokenView.as_view(), name="token"),
]
