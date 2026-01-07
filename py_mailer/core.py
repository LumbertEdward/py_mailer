from abc import ABC, abstractmethod
from typing import List, Optional


class EmailProvider(ABC):

    @abstractmethod
    def send_email(
        self,
        source: str,
        to: str,
        subject: str,
        body: Optional[str] = None,
        html_body: Optional[str] = None,
        attachments: Optional[List] = None,
    ):
        pass

    @abstractmethod
    def send_batch_emails(self, source: str, messages: List[dict]):
        pass
