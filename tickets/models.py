from django.db import models
from events.models import Event
from users.models import User


class Ticket(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event}"