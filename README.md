# py_mailer 📬

**py_mailer** is a provider-agnostic Python email integration layer that enables developers to send emails through multiple providers—such as **Resend** and **SendGrid**—using a single, consistent API.

It abstracts away provider-specific SDKs, making it easy to switch email services without rewriting application logic.

> **Write once. Send anywhere.**

---

## Features

- 🔌 Pluggable email providers (Resend, SendGrid, more coming)
- 🧩 Clean, unified API across providers
- 📤 Single and batch email sending
- 📎 Attachment support (including per-recipient attachments)
- ⚙️ Framework-friendly (FastAPI, Django, Flask)

---

## Installation

```bash
pip install py_mailer
```

---

## Usage

## Initialize a provider

---

```bash
from py_mailer.providers.resend import ResendEmailProvider

mailer = ResendEmailProvider(api_key="re_123")

from py_mailer.providers.brevo import BrevoEmailProvider

mailer = BrevoEmailProvider(
    api_key="BREVO_API_KEY",
    sender_email="billing@yourapp.com",
    sender_name="Your App",
)
```

---

## Sending a single email

---

```bash
mailer.send_email(
    source="noreply@yourapp.com",
    to="user@example.com",
    subject="Welcome",
    html_body="<h1>Hello 👋</h1>",
    attachments=[
        {
            "filename": "invoice.pdf",
            "content": base64_string,
            "type": "application/pdf",
            "path": "/path/to/invoice.pdf",
        }
    ]
)
```

---

## Sending batch emails

Batch emails allow sending messages to multiple recipients in a single request.
Each message may optionally include its own attachments.

---

```bash
mailer.send_batch_emails(
    source="noreply@yourapp.com",
    messages=[
        {
            "to": "user@example.com",
            "subject": "Welcome",
            "html_body": "<h1>Hello 👋</h1>",
            "attachments": [
                {
                    "filename": "invoice.pdf",
                    "content": base64_string,
                    "type": "application/pdf",
                    "path": "/path/to/invoice.pdf",
                }
            ],
        }
    ],
)
```

---

## Attachments

Attachments are passed as a list of dictionaries with the following structure:

---

Resend

```bash
attachments = [
    {
        "filename": "invoice.pdf",
        "content": base64_string,  # Base64-encoded file content
        "type": "application/pdf",
        "path": "/path/to/invoice.pdf",  # Optional
    }
]
```

Brevo

```bash
attachments = [
        {
            "name": "invoice.pdf",
            "content": base64_string,  # base64 encoded
            "type": "application/pdf",
        }
]

Note: py_mailer does not enforce how attachments are generated.
Encoding and file handling are left to the consuming application.
```

---

## Supported Providers

---

✅ Resend
✅ Brevo
