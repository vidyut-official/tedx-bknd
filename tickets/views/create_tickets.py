from django.db import IntegrityError
from django.http import JsonResponse
from ..models import Ticket
def book_ticket(user,event):

    try:

        ticket = Ticket.objects.create(
            event=event,
            user=user
        )

        return JsonResponse({"message": "Ticket booked successfully"}, status=201)


    except IntegrityError:
        return JsonResponse({"error": "You have already booked this event."}, status=400)

    except Exception as e:
        return JsonResponse({"error": "Internal server error"}, status=500)