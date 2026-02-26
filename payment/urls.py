from django.urls import path,include
from .views.make_payment import MakePayment
from .views.verify_payment import VerifyPayment


urlpatterns = [
    path('make/', MakePayment.as_view(),name="make-payment"),
    path('verify/', VerifyPayment.as_view(),name="verify-payment"),
    path('verify/', VerifyPayment.as_view(),name="verify-payment"),

    
]
