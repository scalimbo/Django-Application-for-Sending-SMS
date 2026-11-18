import re

from django import forms


class SmsForm(forms.Form):
    recipient = forms.CharField(
        max_length=20,
        label="Recipient",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter recipient number",
                "class": "form-control",
            }
        ),
    )
    message = forms.CharField(
        max_length=160,
        label="Message",
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Enter your message here",
                "class": "form-control",
                "maxlength": "160",
            }
        ),
    )

    def clean_recipient(self):
        recipient = self.cleaned_data["recipient"].strip()

        if not re.fullmatch(r"\+[1-9][0-9]{7,14}", recipient):
            raise forms.ValidationError(
                "Enter a valid international phone number. "
                "Example: +639171234567"
            )

        return recipient

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if not message:
            raise forms.ValidationError("Message cannot be empty.")

        return message