import requests
from typing import Dict, List, Optional
from py_mailer.core import EmailProvider
from py_mailer.exceptions import ConfigurationError, SendError


class BrevoEmailProvider(EmailProvider):
    BASE_URL = "https://api.brevo.com/v3/smtp/email"

    def __init__(
        self,
        api_key: str,
        sender_email: str,
        sender_name: Optional[str] = None,
        timeout: int = 10,
    ):
        if not api_key:
            raise ConfigurationError("Brevo API key is required")

        if not sender_email:
            raise ConfigurationError("Brevo sender email is required")

        self.api_key = api_key
        self.sender_email = sender_email
        self.sender_name = sender_name
        self.timeout = timeout

        self.headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }

    def send(
        self,
        source: str,
        to: str,
        subject: str,
        html_body: str,
        attachments: Optional[List[Dict]] = None,
    ) -> bool:
        payload = {
            "sender": {
                "email": self.sender_email,
                "name": self.sender_name,
            },
            "to": [{"email": to}],
            "subject": subject,
            "htmlContent": html_body,
        }

        if attachments:
            payload["attachment"] = [
                {
                    "name": att["name"],
                    "content": att["content"],  # base64 encoded
                    "type": att.get("type"),
                    "disposition": "attachment",
                }
                for att in attachments
            ]

        try:
            response = requests.post(
                self.BASE_URL,
                json=payload,
                headers=self.headers,
                timeout=self.timeout,
            )

            if response.status_code == 201:
                return True

            raise SendError(
                f"Brevo API error: {response.status_code} - {response.text}"
            )

        except requests.RequestException as exc:
            raise SendError("Failed to send email via Brevo API") from exc

    def send_batch_emails(self, source: str, messages: List[Dict]) -> List[Dict]:
        responses = []
        for msg in messages:
            try:
                success = self.send(
                    to=msg["to"],
                    subject=msg["subject"],
                    html_body=msg["html_body"],
                    attachments=msg.get("attachments"),
                )
                responses.append(
                    {"to": msg["to"], "status": "sent" if success else "failed"}
                )
            except SendError as exc:
                responses.append({"to": msg["to"], "error": str(exc)})
        return responses
