class MailerError(Exception):
    """Base exception for py-mailer."""


class ConfigurationError(MailerError):
    """Invalid or missing configuration."""


class AuthenticationError(MailerError):
    """Invalid or missing API key."""


class ValidationError(MailerError):
    """Invalid request payload."""


class RateLimitError(MailerError):
    """Provider rate limit exceeded."""


class ProviderError(MailerError):
    """Upstream provider failure."""


class SendError(ProviderError):
    """Failed to send email."""
