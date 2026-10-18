"""Explainable heuristic scoring for possible money-mule accounts."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal


def score_accounts(transactions: list[dict[str, object]], rapid_minutes: int = 60) -> list[dict[str, object]]:
    incoming: dict[str, list[dict[str, object]]] = defaultdict(list)
    outgoing: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in transactions:
        outgoing[str(row["source_account_id"])].append(row)
        incoming[str(row["destination_account_id"])].append(row)

    findings = []
    for account_id in sorted(incoming.keys() & outgoing.keys()):
        credits = incoming[account_id]
        debits = outgoing[account_id]
        received = sum((Decimal(str(row["amount"])) for row in credits), Decimal("0"))
        sent = sum((Decimal(str(row["amount"])) for row in debits), Decimal("0"))
        if not received:
            continue
        first_credit = min(datetime.fromisoformat(str(row["occurred_at"])) for row in credits)
        last_debit = max(datetime.fromisoformat(str(row["occurred_at"])) for row in debits)
        rapid = timedelta(0) <= last_debit - first_credit <= timedelta(minutes=rapid_minutes)
        pass_through = Decimal("0.80") <= sent / received <= Decimal("1.10")
        factors = []
        if len({str(row["source_account_id"]) for row in credits}) >= 2:
            factors.append("MULTIPLE_SENDERS")
        if rapid:
            factors.append("RAPID_MOVEMENT")
        if pass_through:
            factors.append("LOW_RETENTION")
        if len(factors) >= 2:
            findings.append({"account_id": account_id, "score": min(100, len(factors) * 30), "factors": factors})
    return sorted(findings, key=lambda item: (-int(item["score"]), str(item["account_id"])))

