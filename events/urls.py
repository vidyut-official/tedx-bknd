from django.urls import path
from .views.get_all_events import EventListAPIView

urlpatterns = [
    path("all/", EventListAPIView.as_view(), name="event-list"),
]