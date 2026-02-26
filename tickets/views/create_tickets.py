
from ..models import Ticket

def book_ticket(user, event, payment):

    ticket = Ticket.objects.create(
        event=event,
        user=user,
        payment=payment
    )

    return ticket