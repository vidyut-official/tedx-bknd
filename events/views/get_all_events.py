from django.db.models import Count, F
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Event
from tickets.models import Ticket


class EventListAPIView(APIView):

    def get(self, request):

        events = (
            Event.objects
            .annotate(
                tickets_sold=Coalesce(Count("tickets"), 0),
                remaining_seats=F("quantity") - Coalesce(Count("tickets"), 0)
            )
            .values(
                "id",
                "name",
                "quantity",
                "ticket_rate",
                "remaining_seats",
            )
        )

        return Response(list(events))