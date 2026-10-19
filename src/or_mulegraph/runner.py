"""Validated boundary used by the CLI and HTTP adapter."""
from .networks import detect_rings
from .scoring import score_accounts


def run(payload):
    if not isinstance(payload, dict) or set(payload) - set(["transactions","options","action"]):
        raise ValueError("request must be an object containing only documented fields")
    if payload.get("action") == "rings":
        return detect_rings(payload.get("transactions"), **payload.get("options", {}))
    if payload.get("action", "score") != "score":
        raise ValueError("unknown action")
    return score_accounts(payload.get('transactions'), **payload.get('options', {}))
