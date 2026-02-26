from django.urls import path,include
from .views.register_user import RegisterUser

urlpatterns = [
    path('register/', RegisterUser.as_view(),name="register-user")
    
]
