from django.urls import path, reverse

from .views import CreateUserView, CreateTokenView

app_name = 'service'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
]
