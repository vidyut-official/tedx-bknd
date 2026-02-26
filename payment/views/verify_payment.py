from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from ..models import Payment
from tickets.models import Ticket


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

            payment = Payment.objects.select_for_update().get(id=payment_id)

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

            Ticket.objects.create(
                user=payment.user,
                event=payment.event,
                payment=payment
            )

        return Response(
            {
                "message": "Payment verified successfully",
                "verified_by": request.user.username
            },
            status=status.HTTP_200_OK
        )