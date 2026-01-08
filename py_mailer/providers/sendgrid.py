import base64
from typing import Dict, List, Optional

import sendgrid
from sendgrid.helpers.mail import (
    Mail,
    Email,
    To,
    Content,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

from py_mailer.core import EmailProvider
from py_mailer.exceptions import ConfigurationError, SendError


class SendGridEmailProvider(EmailProvider):
    def __init__(
        self,
        api_key: str,
        sender_email: str,
        sender_name: Optional[str] = None,
    ):
        if not api_key:
            raise ConfigurationError("SendGrid API key is required")

        if not sender_email:
            raise ConfigurationError("SendGrid sender email is required")

        self.client = sendgrid.SendGridAPIClient(api_key=api_key)
        self.sender = Email(sender_email, sender_name)

    def send(
        self,
        source: str,
        to: str,
        subject: str,
        body: Optional[str] = None,
        html_body: Optional[str] = None,
        attachments: Optional[List[Dict]] = None,
    ) -> bool:
        if not body and not html_body:
            raise SendError("Either body or html_body must be provided")

        try:
            contents = []
            if body:
                contents.append(Content("text/plain", body))
            if html_body:
                contents.append(Content("text/html", html_body))

            mail = Mail(
                from_email=self.sender,
                to_emails=To(to),
                subject=subject,
            )

            for content in contents:
                mail.add_content(content)

            if attachments:
                for att in attachments:
                    attachment = Attachment(
                        FileContent(att["content"]),  # base64 encoded
                        FileName(att["name"]),
                        FileType(att.get("type", "application/octet-stream")),
                        Disposition("attachment"),
                    )
                    mail.add_attachment(attachment)

            response = self.client.client.mail.send.post(request_body=mail.get())

            if response.status_code in (200, 202):
                return True

            raise SendError(f"SendGrid API error: {response.status_code}")

        except Exception as exc:
            raise SendError("Failed to send email via SendGrid") from exc

    def send_batch_emails(self, source: str, messages: List[dict]) -> List[bool]:
        results = []
        for msg in messages:
            try:
                result = self.send(
                    to=msg.get("to"),
                    subject=msg.get("subject"),
                    body=msg.get("body"),
                    html_body=msg.get("html_body"),
                    attachments=msg.get("attachments"),
                )
                results.append(result)
            except SendError:
                results.append(False)
        return results
