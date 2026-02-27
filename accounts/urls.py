from django.urls import path
from .registration.register_user import registrations_login


urlpatterns = [
    path("login/registrations", registrations_login, name="registrations_login"),
]
