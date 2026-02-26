from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "user", "created_at")
    search_fields = ("event__name", "user__email", "user__full_name")
    list_filter = ("event", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)