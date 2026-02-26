from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from ..models import Payment


class GetAllPayments(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        # Optional filter: ?status=pending
        status_filter = request.query_params.get("status")

        payments = Payment.objects.select_related("user", "event", "verified_by")

        if status_filter:
            payments = payments.filter(payment_status=status_filter)

        data = []

        for payment in payments.order_by("-created_at"):
            data.append({
                "payment_id": payment.id,
                "user": payment.user.username,
                "user_email": payment.user.email,
                "event": payment.event.name,
                "amount": str(payment.amount),
                "status": payment.payment_status,
                "payment_method": payment.payment_method,
                "verified_by": payment.verified_by.username if payment.verified_by else None,
                "verified_at": payment.verified_at,
                "created_at": payment.created_at,
            })

        return Response(
            {
                "count": payments.count(),
                "payments": data
            },
            status=status.HTTP_200_OK
        )