import unittest

from or_mulegraph import project_info, score_accounts


class ProjectSmokeTest(unittest.TestCase):
    def test_project_metadata(self) -> None:
        self.assertEqual(project_info()["status"], "starter")

    def test_scores_pass_through_account(self) -> None:
        rows = [
            {"source_account_id": "x", "destination_account_id": "m", "amount": "500", "occurred_at": "2026-01-01T10:00:00+00:00"},
            {"source_account_id": "y", "destination_account_id": "m", "amount": "500", "occurred_at": "2026-01-01T10:02:00+00:00"},
            {"source_account_id": "m", "destination_account_id": "z", "amount": "950", "occurred_at": "2026-01-01T10:05:00+00:00"},
        ]
        finding = score_accounts(rows)[0]
        self.assertEqual(finding["account_id"], "m")
        self.assertIn("LOW_RETENTION", finding["factors"])



if __name__ == "__main__":
    unittest.main()

