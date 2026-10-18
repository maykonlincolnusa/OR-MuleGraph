"""Starter package for OR MuleGraph."""

from .scoring import score_accounts

__version__ = "0.1.0"


def project_info() -> dict[str, str]:
    return {
        "name": "OR MuleGraph",
        "focus": "Explainable money-mule detection",
        "status": "starter",
    }


__all__ = ["project_info", "score_accounts"]

