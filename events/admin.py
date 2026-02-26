from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("date", "created_at")
    ordering = ("-date",)
    readonly_fields = ("created_at", "updated_at")