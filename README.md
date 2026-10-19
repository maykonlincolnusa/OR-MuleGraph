# OR MuleGraph

Evidence-linked behavioral indicators for potential money-mule accounts.

## Why it matters

Rapid pass-through activity and coordinated counterparties can reveal accounts that deserve investigation. This project scores observable window behavior and always returns the underlying transactions and factor contributions. The score is a queue heuristic, not a calibrated probability.

## Current capabilities

- Rapid movement and high outflow-ratio indicators.
- Multiple-sender and multiple-recipient factors.
- Independent windows for each account and currency.
- Stable alert identifiers, exact decimal arithmetic, and evidence IDs.
- Shared-counterparty ring detection for coordinated hubs, with time and work budgets.
- Clear distinction between observed flows and balance/fund attribution.
- Strict validation, CLI, optional authenticated API, Docker image, and CI.

## Run

```sh
python -m pip install -e '.[dev,api]'
python -m or_mulegraph --demo
pytest -q && ruff check src tests
```

API: set `OR_API_KEY` to at least 16 characters, run `uvicorn or_mulegraph.api:create_app --factory`, then POST `examples/request.json` to `/v1/analyze`.

## Limitations and roadmap

Set `action` to `rings` to run the coordinated-network detector; its response exposes whether the work budget truncated analysis. This rule-based prototype is not trained or calibrated on institutional data. Next steps are cohort-aware features, event-time streaming, feedback capture, and precision/recall evaluation on governed labels.
