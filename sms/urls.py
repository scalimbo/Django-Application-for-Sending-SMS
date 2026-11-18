from django.urls import path

from .views import dashboard_view, send_sms_view

app_name = "sms"

urlpatterns = [
    path("send/", send_sms_view, name="send_sms"),
    path("dashboard/", dashboard_view, name="dashboard"),
]