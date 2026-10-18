"""Deterministic synthetic input; no customer data."""
DEMO = {
    "transactions": [
        {
            "id": "t1",
            "source_account_id": "a",
            "destination_account_id": "hub",
            "amount": "5000.00",
            "currency": "BRL",
            "occurred_at": "2026-01-01T10:00:00Z"
        },
        {
            "id": "t2",
            "source_account_id": "b",
            "destination_account_id": "hub",
            "amount": "5000.00",
            "currency": "BRL",
            "occurred_at": "2026-01-01T10:01:00Z"
        },
        {
            "id": "t3",
            "source_account_id": "hub",
            "destination_account_id": "c",
            "amount": "9500.00",
            "currency": "BRL",
            "occurred_at": "2026-01-01T10:05:00Z"
        },
        {
            "id": "t4",
            "source_account_id": "c",
            "destination_account_id": "a",
            "amount": "9000.00",
            "currency": "BRL",
            "occurred_at": "2026-01-01T10:10:00Z"
        }
    ]
}
