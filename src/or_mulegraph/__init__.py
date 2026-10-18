"""Public API for OR MuleGraph."""

from .scoring import score_accounts

__version__ = "0.2.0"


def project_info() -> dict[str, str]:
    return {
        "name": "OR MuleGraph",
        "focus": "Explainable money-mule detection",
        "status": "reference-prototype",
    }


__all__ = ["project_info", "score_accounts"]

