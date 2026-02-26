from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    # Remove username completely
    username = None

    # Email will be login
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=150)

    USER_TYPE = [
        ("amrita", "Amrita"),
        ("others", "Others"),
    ]

    USER_ROLE = [
        ("registration", "Registration"),
        ("finance", "Finance"),
        ("participant", "Participant"),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE,
        default="others",
    )

    user_role = models.CharField(
        max_length=20,
        choices=USER_ROLE,
        default="participant",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]