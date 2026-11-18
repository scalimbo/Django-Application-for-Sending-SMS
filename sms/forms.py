import re
from django import forms #for creating forms

class SmsForm(forms.Form):
    recipient = forms.CharField(
        max_length=20,label='Recipient', max_length=20, widget=forms.TextInput(
            attrs=
            {placeholder': 'Enter recipient number', "class": "form-control"
             }
        ),
    )
    meassage = forms.CharField(
        max_length=160,
        label="Message",
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Enter your message here",
                "class": "form-control",
            }
        ),
    )

    def clean_recipient(self):
        recipient = self.cleaned_data.get['recipient'].strip()

        if not re.fullmatch(r"\+[1-9][0-9]{7,14}", recipient):
            raise forms.ValidationError(
                "Enter a valid phone number, "
                "Example: +63 912 345 6789"
            )
        return recipient

    def clean_message(self):
        message = self.cleaned_data.get('message').strip()

        if not message:
            raise forms.ValidationError("Message cannot be empty.")
        if len(message) > 160:
            raise forms.ValidationError("Message cannot exceed 160 characters.")
        return message