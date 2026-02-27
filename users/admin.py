from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "full_name",
        "user_type",
        "user_role",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "user_type",
        "user_role",
        "is_staff",
        "is_active",
    )

    ordering = ("email",)
    search_fields = ("email", "full_name")

    # Fields shown in detail view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name",)}),
        ("Role & Type", {"fields": ("user_type", "user_role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when creating a user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "full_name",
                "user_type",
                "user_role",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )


admin.site.register(User, CustomUserAdmin)