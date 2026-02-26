from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from ..models import Payment
from tickets.models import Ticket
from tickets.views.create_tickets import book_ticket


class VerifyPayment(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        payment_id = request.data.get("payment_id")

        if not payment_id:
            return Response(
                {"error": "payment_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            payment = get_object_or_404(
                Payment.objects.select_for_update(),
                id=payment_id
            )

            if payment.payment_status == "completed":
                return Response(
                    {"error": "Payment already verified"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            sold = Ticket.objects.filter(event=payment.event).count()

            if sold >= payment.event.total_seats:
                return Response(
                    {"error": "Event is sold out"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            payment.payment_status = "completed"
            payment.verified_by = request.user
            payment.verified_at = timezone.now()
            payment.save()

            try:
                book_ticket(
                    user=payment.user,
                    event=payment.event,
                    payment=payment
                )
            except IntegrityError:
                return Response(
                    {"error": "Ticket already exists for this user."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                "message": "Payment verified and ticket created",
                "verified_by": request.user.username
            },
            status=status.HTTP_200_OK
        )