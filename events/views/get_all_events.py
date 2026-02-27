from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Event


class EventListAPIView(APIView):

    def get(self, request):
        events = Event.objects.all().values("id", "name","quantity","ticket_rate")
        return Response(list(events))