from typing import Union
import resend
from py_mailer.core import EmailProvider
from py_mailer.exceptions import ConfigurationError
from resend.exceptions import ResendError
from py_mailer.errors.resend_errors import translate_resend_error


class ResendEmailProvider(EmailProvider):
    def __init__(self, api_key: str):
        if not api_key:
            raise ConfigurationError("Resend API key is required")
        resend.api_key = api_key

    def send_email(
        self,
        source: str,
        to: str,
        subject: str,
        body: Union[str, None] = None,
        html_body: Union[str, None] = None,
        attachments: Union[list, None] = None,
    ):
        if not (body or html_body):
            raise ConfigurationError("Either body or html_body must be provided")
        params: resend.Emails.SendParams = {
            "from": source,
            "to": to,
            "subject": subject,
        }
        if body:
            params["text"] = body
        if html_body:
            params["html"] = html_body
        if attachments:
            params["attachments"] = attachments

        try:
            return resend.Emails.send(params)
        except ResendError as exc:
            translate_resend_error(exc)

    def send_batch_emails(self, source: str, messages: list):
        responses = []
        for msg in messages:
            params: resend.Emails.SendParams = {
                "from": source,
                "to": msg.get("to"),
                "subject": msg.get("subject"),
            }
            if msg.get("body"):
                params["text"] = msg.get("body")
            if msg.get("html_body"):
                params["html"] = msg.get("html_body")
            if msg.get("attachments"):
                params["attachments"] = msg.get("attachments")
            responses.append(params)
        try:
            return resend.batch.send(responses)
        except ResendError as exc:
            translate_resend_error(exc)
