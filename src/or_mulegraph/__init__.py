"""Public API for OR MuleGraph."""

from .networks import detect_rings
from .scoring import score_accounts

__version__ = "0.3.0"


def project_info() -> dict[str, str]:
    return {
        "name": "OR MuleGraph",
        "focus": "Explainable money-mule detection",
        "status": "reference-prototype",
    }


__all__ = ["detect_rings", "project_info", "score_accounts"]

