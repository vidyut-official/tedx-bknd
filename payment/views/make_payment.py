



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404

from events.models import Event
from models import Payment
from tickets.models import Ticket


class MakePayment(APIView):

    def post(self, request):

        user = request.user
        event_id = request.data.get("event_id")
        quantity = request.data.get("quantity","1")
        payment_method = request.data.get("payment_method")

        # -------- Basic Validation --------
        if not event_id or not quantity:
            return Response(
                {"error": "event_id and quantity required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except:
            return Response(
                {"error": "quantity must be positive integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        event = get_object_or_404(Event, id=event_id)

        # -------- Seat Availability Check --------
        sold_tickets = Ticket.objects.filter(event=event).count()

        if sold_tickets + quantity > event.total_seats:
            return Response(
                {"error": "Not enough seats available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------- Create Payment --------
        with transaction.atomic():

            total_amount = event.ticket_price * quantity

            payment = Payment.objects.create(
                user=user,
                event=event,
                amount=total_amount,
                payment_method=payment_method or "inhand",
                payment_status="pending"
            )

        return Response(
            {
                "message": "Payment created successfully",
                "payment_id": payment.id,
                "amount": payment.amount,
                "status": payment.payment_status
            },
            status=status.HTTP_201_CREATED
        )