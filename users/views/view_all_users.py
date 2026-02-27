from django.http import JsonResponse
from ..models import User


def participants_list(request):
    participants = User.objects.filter(user_role="participant")

    data = list(
        participants.values(
            "id",
            "email",
            "full_name",
            "user_type",
            "user_role",
        )
    )

    return JsonResponse(data, safe=False)