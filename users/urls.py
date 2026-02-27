from django.urls import path,include
from .views.register_user import RegisterUser
from .views.view_all_users import participants_list

urlpatterns = [
    path('register/', RegisterUser.as_view(),name="register-user"),
    path("participants/", participants_list, name="participants_list"),
    
]
