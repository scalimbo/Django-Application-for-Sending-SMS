# Django SMS Application

This is a Django web application project for sending and tracking SMS messages through the
[Infobip SMS API](https://www.infobip.com/docs/api/channels/sms/sms-messaging).
The application validates recipient numbers, submits messages to Infobip, and
records the provider response and delivery status in SQLite.

## Features

- Send SMS messages from a web form.
- Validate recipients in international E.164 format, such as
  `+639171234567`.
- Limits the messages to 160 characters per messages.
- Uses Infobip as the SMS gateway.
- Records pending, sent, and failed messages.
- View recent messages and failed-message details on the SMS dashboard.

## Requirements

- Python 3.10 or newer
- An Infobip account with an SMS API key and sender
- The dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository and open a terminal in the project
   directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On Windows:

   ```powershell
   .venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root. This file is ignored by Git and
   should not be committed:

   ```dotenv
   INFOBIP_BASE_URL=https://your-api-base-url
   INFOBIP_API_KEY=your-infobip-api-key
   INFOBIP_SENDER=your-approved-sender
   ```

   Use the base URL provided for your Infobip account. Do not include
   `/sms/2/text/advanced`; the application appends that endpoint itself.

5. Apply the database migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Open <http://127.0.0.1:8000/> in a browser.

## Infobip integration

When a valid form is submitted, the application sends a `POST` request to:

```text
{INFOBIP_BASE_URL}/sms/2/text/advanced
```

The request uses the `Authorization: App <INFOBIP_API_KEY>` header and sends
the recipient, sender, and message in Infobip's advanced SMS JSON format.
Infobip's response is stored with the message ID and provider status. HTTP
errors, connection errors, invalid responses, and incomplete configuration are
recorded as failed messages.

The Infobip API key, base url, and sender number was not inputted directly in the source code and the `.env`file was not committed to github.

## Application URLs

| URL               | Description                        |
| ----------------- | ---------------------------------- |
| `/`               | Redirects to the send-SMS form     |
| `/sms/send/`      | Send an SMS                        |
| `/sms/dashboard/` | View SMS history and status counts |
| `/admin/`         | Django administration              |

## Project structure

```text
myproject/       Django project settings and URL configuration
sms/             SMS form, Infobip integration, model, and URLs
shop/            Templates and static files for the SMS interface
db.sqlite3       Local SQLite database (created by migrations)
manage.py        Django command-line utility
requirements.txt Python dependencies
```

## Useful commands

```bash
# Create migrations after changing models
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run the test suite
python manage.py test
```

For production, set `DEBUG=False`, configure `ALLOWED_HOSTS`, use a secure
`SECRET_KEY`, and deploy behind a production-ready web server.
