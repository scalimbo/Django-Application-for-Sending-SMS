from django.contrib import admin
from .models import SmsMessage


@admin.register(SmsMessage)
class SmsMessageAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "status",
        "provider_status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("recipient", "text", "provider_message_id")
