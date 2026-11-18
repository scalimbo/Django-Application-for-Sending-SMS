import requests
import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

from .forms import SmsForm
from .models import SmsMessage

logger = logging.getLogger(__name__)


def send_sms_view(request):
    form = SmsForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            recipient = form.cleaned_data["recipient"]
            message_text = form.cleaned_data["message"]

            infobip_base_url = settings.INFOBIP_BASE_URL
            infobip_api_key = settings.INFOBIP_API_KEY
            infobip_sender = settings.INFOBIP_SENDER

            if not all([
                infobip_base_url,
                infobip_api_key,
                infobip_sender,
            ]):
                SmsMessage.objects.create(
                    recipient=recipient,
                    text=message_text,
                    status=SmsMessage.Status.FAILED,
                    error_message="Infobip SMS configuration is incomplete.",
                )
                messages.error(
                    request,
                    "SMS configuration is incomplete.",
                )
                return render(
                    request,
                    "shop/send_sms.html",
                    {"form": form},
                )

            infobip_url = (
                infobip_base_url.rstrip("/")
                + "/sms/2/text/advanced"
            )

            headers = {
                "Authorization": f"App {infobip_api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            payload = {
                "messages": [
                    {
                        "destinations": [
                            {
                                "to": recipient.lstrip("+"),
                            }
                        ],
                        "from": infobip_sender,
                        "text": message_text,
                    }
                ]
            }

            try:
                response = requests.post(
                    infobip_url,
                    headers=headers,
                    json=payload,
                    timeout=15,
                )

                if response.ok:
                    response_data = response.json()
                    provider_message = response_data.get("messages", [{}])[0]
                    provider_status = (
                        provider_message.get("status", {}).get("groupName", "")
                        or provider_message.get("status", {}).get("name", "")
                    )
                    provider_message_id = provider_message.get("messageId", "")

                    normalized_status = provider_status.upper()
                    if normalized_status in {
                        "REJECTED",
                        "FAILED",
                        "UNDELIVERABLE",
                        "EXPIRED",
                    }:
                        sms_status = SmsMessage.Status.FAILED
                    elif normalized_status in {
                        "PENDING",
                        "WAITING",
                        "QUEUED",
                        "ACCEPTED",
                        "SENT",
                    }:
                        sms_status = (
                            SmsMessage.Status.SENT
                            if normalized_status in {"SENT", "ACCEPTED"}
                            else SmsMessage.Status.PENDING
                        )
                    else:
                        sms_status = SmsMessage.Status.PENDING

                    SmsMessage.objects.create(
                        recipient=recipient,
                        text=message_text,
                        status=sms_status,
                        provider_message_id=provider_message_id,
                        provider_status=provider_status,
                    )
                    messages.success(
                        request,
                        "Your message was submitted successfully.",
                    )
                    form = SmsForm()
                else:
                    SmsMessage.objects.create(
                        recipient=recipient,
                        text=message_text,
                        status=SmsMessage.Status.FAILED,
                        error_message=f"Infobip returned HTTP {response.status_code}.",
                    )
                    logger.error(
                        "Infobip rejected an SMS request with status %s.",
                        response.status_code,
                    )
                    messages.error(
                        request,
                        "Infobip rejected the SMS request.",
                    )
            except requests.RequestException as exc:
                SmsMessage.objects.create(
                    recipient=recipient,
                    text=message_text,
                    status=SmsMessage.Status.FAILED,
                    error_message="Unable to connect to the SMS gateway.",
                )
                logger.error("Unable to connect to Infobip: %s", exc)
                messages.error(
                    request,
                    "Unable to connect to the SMS gateway.",
                )
            except ValueError:
                SmsMessage.objects.create(
                    recipient=recipient,
                    text=message_text,
                    status=SmsMessage.Status.FAILED,
                    error_message="Infobip returned an invalid response.",
                )
                messages.error(
                    request,
                    "The SMS gateway returned an invalid response.",
                )

    return render(
        request,
        "shop/send_sms.html",
        {"form": form},
    )


def dashboard_view(request):
    recent_messages = SmsMessage.objects.all()[:20]
    failed_messages = SmsMessage.objects.filter(
        status=SmsMessage.Status.FAILED
    )[:10]

    context = {
        "recent_messages": recent_messages,
        "failed_messages": failed_messages,
        "sent_count": SmsMessage.objects.filter(
            status__in=[
                SmsMessage.Status.SENT,
                SmsMessage.Status.PENDING,
            ]
        ).count(),
        "failed_count": SmsMessage.objects.filter(
            status=SmsMessage.Status.FAILED
        ).count(),
    }

    return render(
        request,
        "shop/sms_dashboard.html",
        context,
    )