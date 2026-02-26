from django.db import models
from events.models import Event
from users.models import User
from payment.models import Payment

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    ticket_code = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)