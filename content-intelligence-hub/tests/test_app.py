import unittest
import app


class ContentIntelligenceMVPTests(unittest.TestCase):
    def test_search_finds_existing_tbs_intelligence(self):
        records = [
            {
                "title": "Strong business, weak online representation",
                "record_type": "Founder Observation",
                "raw_input": "A founder can have a substantial business while their online presence makes them look early-stage.",
                "source": "TBS editorial observation",
                "evidence_status": "Inferred",
            },
            {
                "title": "More content will not fix weak positioning",
                "record_type": "Founder Observation",
                "raw_input": "Increasing posting volume does not repair unclear representation.",
                "source": "TBS content system",
                "evidence_status": "Inferred",
            },
        ]
        results = app.search(records, "strong business weak online presence")
        self.assertEqual(results[0]["title"], "Strong business, weak online representation")

    def test_search_returns_no_match_when_intelligence_is_missing(self):
        records = [{
            "title": "LinkedIn representation",
            "record_type": "Founder Observation",
            "raw_input": "Representation comes before visibility.",
        }]
        self.assertEqual(app.search(records, "industrial export pricing model"), [])

    def test_search_is_case_insensitive(self):
        records = [{
            "title": "Buyer Visibility",
            "record_type": "Buyer Insight",
            "raw_input": "Buyers need to recognize the business before engaging.",
        }]
        results = app.search(records, "buyer visibility")
        self.assertEqual(len(results), 1)

    def test_available_pool_excludes_scheduled_content(self):
        records = [
            {"id": "1", "title": "Available", "lifecycle_status": "Approved", "scheduled_date": ""},
            {"id": "2", "title": "Scheduled", "lifecycle_status": "Scheduled", "scheduled_date": "2026-09-29"},
        ]
        self.assertEqual([r["title"] for r in app.available_records(records)], ["Available"])

    def test_calendar_selection_requires_approval(self):
        records = [{"id": "1", "title": "Draft", "lifecycle_status": "Captured"}]
        target = next(r for r in records if r["id"] == "1")
        self.assertNotEqual(target["lifecycle_status"], "Approved")

    def test_scheduled_content_is_in_calendar_and_out_of_inventory(self):
        records = [{
            "id": "1", "title": "Approved post", "lifecycle_status": "Scheduled",
            "scheduled_date": "2026-09-29", "scheduled_slot": "Tuesday, TOFU",
        }]
        self.assertEqual(app.available_records(records), [])
        self.assertEqual(len(app.calendar_records(records)), 1)
        self.assertEqual(app.calendar_records(records)[0]["scheduled_slot"], "Tuesday, TOFU")


if __name__ == "__main__":
    unittest.main()
