from resend.exceptions import ResendError
from py_mailer.exceptions import (
    AuthenticationError,
    ValidationError,
    ConfigurationError,
    RateLimitError,
    ProviderError,
    SendError,
)


def translate_resend_error(exc: ResendError) -> None:
    """
    Translate Resend SDK errors into py-mailer exceptions.
    """
    code = getattr(exc, "code", None)
    error_type = getattr(exc, "error_type", None)
    message = str(exc)

    # --- AUTH / CONFIG ---
    if code == 401:
        raise AuthenticationError(message) from exc

    if error_type in {"missing_api_key", "invalid_api_key"}:
        raise AuthenticationError(message) from exc

    # --- VALIDATION ---
    if error_type in {"validation_error", "missing_required_fields"}:
        raise ValidationError(message) from exc

    # --- RATE LIMIT ---
    if code == 429:
        raise RateLimitError(message) from exc

    # --- PROVIDER / APPLICATION ---
    if error_type == "application_error":
        raise ProviderError(message) from exc

    # --- FALLBACK ---
    raise SendError(message) from exc
