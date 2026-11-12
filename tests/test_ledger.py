"""Tests for scripts/ledger.py. Every value below is invented."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import ledger  # noqa: E402


def entry(i, **kw):
    e = {"id": f"e-{i:06d}", "date": "2099-01-05", "slot": "lunch", "food_id": "sample-grain",
         "amount": 100, "unit": "g", "status": "weighed"}
    e.update(kw)
    return e


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "ledger.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def test_append_adds_lines_and_never_rewrites(self):
        ledger.append(self.path, entry(1))
        first = self.path.read_bytes()
        ledger.append(self.path, entry(2))
        self.assertTrue(self.path.read_bytes().startswith(first))
        self.assertEqual(len(ledger.read(self.path)), 2)

    def test_labels_are_exactly_the_four_published_words(self):
        self.assertEqual(ledger.LABELS, ("label", "weighed", "estimate", "unconfirmed"))
        for bad in ("guess", "Weighed", "database", "", None):
            with self.assertRaises(ledger.LedgerError):
                ledger.validate(entry(1, status=bad))

    def test_missing_amount_stays_missing(self):
        ledger.append(self.path, entry(1, amount=None, status="unconfirmed"))
        got = ledger.read(self.path)[0]
        self.assertIsNone(got["amount"])
        self.assertIn('"amount": null', self.path.read_text(encoding="utf-8"))

    def test_amount_must_be_present_as_a_field(self):
        e = entry(1)
        del e["amount"]
        with self.assertRaises(ledger.LedgerError):
            ledger.validate(e)

    def test_estimate_needs_a_range_around_the_amount(self):
        with self.assertRaises(ledger.LedgerError):
            ledger.validate(entry(1, status="estimate"))
        with self.assertRaises(ledger.LedgerError):
            ledger.validate(entry(1, status="estimate", range=[120, 150]))
        ledger.validate(entry(1, status="estimate", range=[80, 120]))

    def test_ids_are_never_reused(self):
        ledger.append(self.path, entry(1))
        with self.assertRaises(ledger.LedgerError):
            ledger.append(self.path, entry(1, amount=50))
        self.assertEqual(len(ledger.read(self.path)), 1)

    def test_correction_is_a_new_line_and_the_old_line_is_kept(self):
        ledger.append(self.path, entry(1))
        ledger.append(self.path, entry(2, amount=80, corrects="e-000001"))
        lines = self.path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(json.loads(lines[0])["amount"], 100)
        cur = ledger.current(ledger.read(self.path))
        self.assertEqual([e["id"] for e in cur], ["e-000002"])

    def test_correction_chain_keeps_only_the_last(self):
        ledger.append(self.path, entry(1))
        ledger.append(self.path, entry(2, corrects="e-000001"))
        ledger.append(self.path, entry(3, corrects="e-000002"))
        self.assertEqual([e["id"] for e in ledger.current(ledger.read(self.path))], ["e-000003"])

    def test_correction_must_point_at_an_existing_entry(self):
        with self.assertRaises(ledger.LedgerError):
            ledger.append(self.path, entry(2, corrects="e-000999"))

    def test_bad_values_are_refused(self):
        for kw in ({"unit": "oz"}, {"date": "05/01/2099"}, {"amount": -1}, {"amount": "100"}, {"amount": True}):
            with self.assertRaises(ledger.LedgerError):
                ledger.validate(entry(1, **kw))

    def test_meta_line_is_not_an_entry(self):
        self.path.write_text('{"meta": "synthetic", "note": "invented"}\n', encoding="utf-8")
        ledger.append(self.path, entry(1))
        self.assertEqual(len(ledger.read(self.path)), 1)

    def test_bad_line_reports_its_number(self):
        self.path.write_text(json.dumps(entry(1)) + "\n{not json\n", encoding="utf-8")
        with self.assertRaisesRegex(ledger.LedgerError, "line 2"):
            ledger.read(self.path)


if __name__ == "__main__":
    unittest.main()
