import requests
import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render

from .forms import SmsForm

logger = logging.getLogger(__name__)


def send_sms_view(request):
    form = SmsForm()

    if request.method == "POST":
        form = SmsForm(request.POST)

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
                raise ImproperlyConfigured(
                    "Infobip environment variables are missing."
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
                    messages.success(
                        request,
                        "Your message was submitted successfully.",
                    )
                    form = SmsForm()
                else:
                    logger.error(
                        "Infobip rejected an SMS request with status %s.",
                        response.status_code,
                    )
                    messages.error(
                        request,
                        "Infobip rejected the SMS request.",
                    )
            except requests.RequestException as exc:
                logger.error("Unable to connect to Infobip: %s", exc)
                messages.error(
                    request,
                    "Unable to connect to the SMS gateway.",
                )

    return render(
        request,
        "shop/send_sms.html",
        {"form": form},
    )