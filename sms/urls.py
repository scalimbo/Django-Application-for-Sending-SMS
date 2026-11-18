from django.urls import path

from .views import send_sms_view

app_name = "sms"

urlpatterns = [
    path("send/", send_sms_view, name="send_sms"),
]