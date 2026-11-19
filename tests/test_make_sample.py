"""Tests for scripts/make_sample.py: the sample is reproducible, labelled synthetic and follows the ledger rules."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import ledger  # noqa: E402
import make_sample  # noqa: E402


class MakeSampleTests(unittest.TestCase):
    def test_same_seed_same_bytes(self):
        a = make_sample.render(make_sample.build(seed=7))
        b = make_sample.render(make_sample.build(seed=7))
        self.assertEqual(a, b)
        self.assertNotEqual(a, make_sample.render(make_sample.build(seed=8)))

    def test_committed_sample_matches_a_fresh_run(self):
        self.assertEqual(make_sample.main(["--check", "--out", str(ROOT / "data" / "sample")]), 0)

    def test_files_say_synthetic_at_the_top(self):
        files = make_sample.render(make_sample.build())
        for name, text in files.items():
            self.assertIn("synthetic", name)
            first = json.loads(text.splitlines()[0]) if name.endswith(".jsonl") else json.loads(text)
            self.assertEqual(first["meta"], "synthetic")

    def test_dates_are_clearly_fictional(self):
        for e in make_sample.build():
            self.assertTrue(e["date"].startswith("2099-"), e["date"])

    def test_sample_follows_the_ledger_rules(self):
        with tempfile.TemporaryDirectory() as t:
            make_sample.main(["--out", t])
            entries = ledger.read(Path(t) / "ledger.synthetic.jsonl")
        self.assertTrue(entries)
        self.assertEqual({e["status"] for e in entries}, set(ledger.LABELS))

    def test_awkward_cases_are_present(self):
        entries = make_sample.build()
        self.assertTrue(any(e["amount"] is None for e in entries), "a missing amount")
        self.assertTrue(any("corrects" in e for e in entries), "a correction")
        dates = {e["date"] for e in entries}
        self.assertLess(len(dates), 30, "at least one day with nothing logged")
        foods = {f["food_id"]: f for f in make_sample.FOODS}
        self.assertTrue(any(v is None for f in foods.values() for v in f["nutrients"].values()), "a blank nutrient")


if __name__ == "__main__":
    unittest.main()
