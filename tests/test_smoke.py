import unittest

from or_mulegraph import project_info, score_accounts


def tx(identifier, source, target, amount, currency="BRL", minute=0):
    return {"id": identifier, "source_account_id": source, "destination_account_id": target,
            "amount": amount, "currency": currency,
            "occurred_at": f"2026-01-01T10:{minute:02d}:00+00:00"}


class ProjectTest(unittest.TestCase):
    def test_scores_pass_through_account_with_evidence(self):
        rows = [tx("1", "x", "m", "500", minute=0), tx("2", "y", "m", "500", minute=2),
                tx("3", "m", "z", "950", minute=5)]
        finding = score_accounts(rows)[0]
        self.assertIn("HIGH_OUTFLOW_RATIO", finding["factors"])
        self.assertEqual(finding["transaction_ids"], ["1", "2", "3"])
        self.assertEqual(project_info()["status"], "reference-prototype")

    def test_does_not_mix_currencies(self):
        rows = [tx("1", "x", "m", "500", "BRL", 0), tx("2", "m", "z", "500", "USD", 5)]
        self.assertEqual(score_accounts(rows), [])

    def test_rejects_duplicate_transaction_ids(self):
        with self.assertRaises(ValueError):
            score_accounts([tx("1", "x", "m", "1"), tx("1", "m", "z", "1", minute=1)])


if __name__ == "__main__":
    unittest.main()
