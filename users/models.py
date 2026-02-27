from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager










class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, full_name, password, **extra_fields)


















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
        ("admin", "Admin"),
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
    objects = CustomUserManager()





