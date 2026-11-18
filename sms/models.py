from django.db import models


class SmsMessage(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    recipient = models.CharField(max_length=20)
    text = models.TextField(max_length=160)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    provider_message_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )
    provider_status = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )
    error_message = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient} - {self.status}"
