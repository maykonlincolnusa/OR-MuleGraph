from or_mulegraph.networks import detect_rings


def row(identifier, source, target, minute):
    return {"id": identifier, "source_account_id": source,
            "destination_account_id": target, "amount": "100", "currency": "BRL",
            "occurred_at": f"2026-01-01T10:{minute:02d}:00Z"}


def test_detects_hubs_with_shared_senders_and_recipients():
    rows = [row("1", "s1", "h1", 0), row("2", "s2", "h1", 1),
            row("3", "s1", "h2", 2), row("4", "s2", "h2", 3),
            row("5", "h1", "r1", 4), row("6", "h1", "r2", 5),
            row("7", "h2", "r1", 6), row("8", "h2", "r2", 7)]
    result = detect_rings(rows)
    assert result["alerts"][0]["account_ids"] == ["h1", "h2"]
    assert result["truncated"] is False


def test_exposes_work_budget_truncation():
    result = detect_rings([row("1", "s", "h", 0), row("2", "h", "r", 1)],
                          max_pair_checks=1)
    assert result["truncated"] is True
