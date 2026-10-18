"""Validated boundary used by the CLI and HTTP adapter."""
from .scoring import score_accounts


def run(payload):
    if not isinstance(payload, dict) or set(payload) - set(["transactions","options"]):
        raise ValueError("request must be an object containing only documented fields")
    return score_accounts(payload.get('transactions'), **payload.get('options', {}))
