"""Shared-counterparty rings with explicit time, currency and work budgets."""
from collections import defaultdict
from datetime import timedelta
from hashlib import sha256

from .validation import instant, integer, transactions


def detect_rings(rows, window_minutes=60, min_shared=2, min_accounts=2,
                 max_pair_checks=100000):
    integer(window_minutes, "window_minutes", 1, 1440)
    integer(min_shared, "min_shared", 1, 100)
    integer(min_accounts, "min_accounts", 2, 100)
    integer(max_pair_checks, "max_pair_checks", 1, 1000000)
    groups = defaultdict(list)
    for row in transactions(rows):
        groups[row["currency"]].append(row)
    alerts, seen, checks = [], set(), 0
    for unit, events in sorted(groups.items()):
        for start in sorted({instant(row["occurred_at"]) for row in events}):
            # Candidate windows count against the budget even for sparse networks.
            if checks >= max_pair_checks:
                return {"alerts": alerts, "truncated": True, "work_units": checks}
            checks += 1
            end = start + timedelta(minutes=window_minutes)
            credits, debits = defaultdict(list), defaultdict(list)
            for row in events:
                if start <= instant(row["occurred_at"]) <= end:
                    credits[row["destination_account_id"]].append(row)
                    debits[row["source_account_id"]].append(row)
            hubs = sorted(credits.keys() & debits.keys())
            neighbors = defaultdict(set)
            for index, left in enumerate(hubs):
                for right in hubs[index + 1:]:
                    if checks >= max_pair_checks:
                        return {"alerts": alerts, "truncated": True, "work_units": checks}
                    checks += 1
                    senders = {r["source_account_id"] for r in credits[left]} & {
                        r["source_account_id"] for r in credits[right]}
                    receivers = {r["destination_account_id"] for r in debits[left]} & {
                        r["destination_account_id"] for r in debits[right]}
                    if len(senders) >= min_shared and len(receivers) >= min_shared:
                        neighbors[left].add(right)
                        neighbors[right].add(left)
            visited = set()
            for origin in sorted(neighbors):
                if origin in visited:
                    continue
                component, stack = set(), [origin]
                while stack:
                    node = stack.pop()
                    if node in component:
                        continue
                    component.add(node)
                    stack.extend(neighbors[node] - component)
                visited.update(component)
                if len(component) < min_accounts:
                    continue
                ids = sorted({r["id"] for account in component
                              for r in credits[account] + debits[account]})
                signature = (unit, tuple(sorted(component)), tuple(ids))
                if signature in seen:
                    continue
                seen.add(signature)
                alerts.append({"id": "ring-" + sha256(repr(signature).encode()).hexdigest()[:20],
                               "rule": "SHARED_COUNTERPARTY_RING", "rule_version": "3.0",
                               "currency": unit, "account_ids": sorted(component),
                               "transaction_ids": ids, "window_start": start.isoformat(),
                               "window_end": end.isoformat(),
                               "explanation": "Connected hubs share senders and recipients; legitimate collection networks can also match."})
    return {"alerts": alerts, "truncated": False, "work_units": checks}
