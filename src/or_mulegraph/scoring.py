"""Window-based, evidence-linked money-mule indicators; not a calibrated model."""
from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
from decimal import Decimal
from hashlib import sha256

from .validation import instant, integer, transactions

RULE_VERSION = "2.0"


def score_accounts(transactions_input, rapid_minutes=60):
    integer(rapid_minutes, "rapid_minutes", 1, 1440)
    incoming, outgoing = defaultdict(list), defaultdict(list)
    for row in transactions(transactions_input):
        incoming[(row["destination_account_id"], row["currency"])].append(row)
        outgoing[(row["source_account_id"], row["currency"])].append(row)
    findings = []
    for (account, unit) in sorted(incoming.keys() & outgoing.keys()):
        credits, debits = incoming[(account, unit)], outgoing[(account, unit)]
        best = None
        for anchor in credits:
            start = instant(anchor["occurred_at"])
            end = start + timedelta(minutes=rapid_minutes)
            selected_in = [r for r in credits if start <= instant(r["occurred_at"]) <= end]
            selected_out = [r for r in debits if start < instant(r["occurred_at"]) <= end]
            if not selected_out:
                continue
            # Do not use credits received after the final observed debit.
            last_out = max(instant(r["occurred_at"]) for r in selected_out)
            selected_in = [r for r in selected_in if instant(r["occurred_at"]) < last_out]
            received = sum((Decimal(r["amount"]) for r in selected_in), Decimal("0"))
            sent = sum((Decimal(r["amount"]) for r in selected_out), Decimal("0"))
            ratio = sent / received
            factors = ["RAPID_MOVEMENT"]
            if Decimal("0.80") <= ratio <= Decimal("1.10"):
                factors.append("HIGH_OUTFLOW_RATIO")
            if len({r["source_account_id"] for r in selected_in}) >= 2:
                factors.append("MULTIPLE_SENDERS")
            if len({r["destination_account_id"] for r in selected_out}) >= 3:
                factors.append("MULTIPLE_RECIPIENTS")
            if len(factors) < 2:
                continue
            ids = sorted(r["id"] for r in selected_in + selected_out)
            identity = sha256(repr((account, unit, ids, rapid_minutes)).encode()).hexdigest()[:20]
            finding = {
                "id": "mule-" + identity, "account_id": account, "currency": unit,
                "score": min(100, len(factors) * 25), "factors": factors,
                "rule_version": RULE_VERSION, "transaction_ids": ids,
                "window_start": start.isoformat(), "window_end": last_out.isoformat(),
                "received": format(received, "f"), "sent": format(sent, "f"),
                "outflow_ratio": format(ratio.quantize(Decimal("0.0001")), "f"),
                "explanation": "Observed window activity only; outflow ratio is not a balance or proof of fund attribution.",
            }
            if best is None or finding["score"] > best["score"]:
                best = finding
        if best is not None:
            findings.append(best)
    return sorted(findings, key=lambda item: (-item["score"], item["account_id"], item["currency"]))

