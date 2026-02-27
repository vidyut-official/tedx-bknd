
from ..models import User


def get_user(user_id):
    return User.objects.filter(id=user_id).first()
