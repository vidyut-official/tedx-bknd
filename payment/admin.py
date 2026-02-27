from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "event",
        "amount",
        "payment_method",
        "payment_status",
        "accepted_by",
        "verified_by",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "payment_method",
        "created_at",
        "event",
    )

    search_fields = (
        "user__email",
        "user__full_name",
        "event__name",  # make sure Event has 'name' field
    )

    ordering = ("-created_at",)

    autocomplete_fields = (
        "user",
        "event",
        "accepted_by",
        "verified_by",
    )

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Payment Info", {
            "fields": (
                "event",
                "user",
                "amount",
                "payment_method",
                "payment_status",
            )
        }),
        ("Approval Info", {
            "fields": (
                "accepted_by",
                "verified_by",
            )
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )