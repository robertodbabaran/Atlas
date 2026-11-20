"""Tests for scripts/export.py. Small invented inputs, plus one run on the synthetic sample."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import export  # noqa: E402

CATALOGUE = {"foods": [
    {"food_id": "a", "name": "A", "per": "100 g", "nutrients": {"energy_kcal": 100, "protein_g": 10.0}},
    {"food_id": "b", "name": "B", "per": "1 item", "nutrients": {"energy_kcal": 50, "protein_g": None}},
]}


def e(i, day, food="a", amount=100, unit="g", status="weighed", **kw):
    d = {"id": f"e-{i}", "date": day, "slot": "lunch", "food_id": food, "amount": amount,
         "unit": unit, "status": status}
    d.update(kw)
    return d


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        (self.dir / "cat.json").write_text(json.dumps(CATALOGUE), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_export(self, entries, as_of="2099-01-10", stale_after=3):
        p = self.dir / "ledger.jsonl"
        p.write_text("".join(json.dumps(x) + "\n" for x in entries), encoding="utf-8")
        days, fresh = export.export(p, self.dir / "cat.json", as_of, stale_after)
        return {d["date"]: d for d in days}, fresh

    def test_simple_total(self):
        days, _ = self.run_export([e(1, "2099-01-01", amount=250)])
        n = days["2099-01-01"]["nutrients"]
        self.assertEqual(n["energy_kcal"]["value"], 250.0)
        self.assertEqual(n["protein_g"]["value"], 25.0)

    def test_missing_amount_makes_the_total_missing_not_lower(self):
        days, _ = self.run_export([e(1, "2099-01-01"), e(2, "2099-01-01", amount=None, status="unconfirmed")])
        en = days["2099-01-01"]["nutrients"]["energy_kcal"]
        self.assertIsNone(en["value"])
        self.assertEqual((en["known_sum"], en["missing_inputs"]), (100.0, 1))

    def test_blank_catalogue_value_stays_missing(self):
        days, _ = self.run_export([e(1, "2099-01-01", food="b", amount=1, unit="item", status="label")])
        n = days["2099-01-01"]["nutrients"]
        self.assertEqual(n["energy_kcal"]["value"], 50.0)
        self.assertIsNone(n["protein_g"]["value"])

    def test_unknown_food_and_wrong_unit_are_missing(self):
        days, _ = self.run_export([e(1, "2099-01-01", food="zzz"), e(2, "2099-01-02", unit="ml")])
        self.assertIsNone(days["2099-01-01"]["nutrients"]["energy_kcal"]["value"])
        self.assertIsNone(days["2099-01-02"]["nutrients"]["energy_kcal"]["value"])

    def test_day_with_nothing_is_absent_and_listed(self):
        days, fresh = self.run_export([e(1, "2099-01-01"), e(2, "2099-01-03")])
        self.assertNotIn("2099-01-02", days)
        self.assertEqual(fresh["days_without_entries"], ["2099-01-02"])

    def test_weakest_label_wins(self):
        days, _ = self.run_export([e(1, "2099-01-01"), e(2, "2099-01-01", status="estimate", range=[80, 120])])
        self.assertEqual(days["2099-01-01"]["label"], "estimate")
        self.assertEqual(export.weakest(["label", "weighed"]), "weighed")
        self.assertEqual(export.weakest(["estimate", "unconfirmed", "label"]), "unconfirmed")

    def test_estimate_range_is_carried_through(self):
        days, _ = self.run_export([e(1, "2099-01-01", status="estimate", range=[80, 120])])
        en = days["2099-01-01"]["nutrients"]["energy_kcal"]
        self.assertEqual((en["low"], en["value"], en["high"]), (80.0, 100.0, 120.0))

    def test_correction_replaces_the_old_line(self):
        days, _ = self.run_export([e(1, "2099-01-01", amount=300), e(2, "2099-01-01", amount=200, corrects="e-1")])
        self.assertEqual(days["2099-01-01"]["nutrients"]["energy_kcal"]["value"], 200.0)
        self.assertEqual(days["2099-01-01"]["entries"], 1)

    def test_freshness_flags_a_stale_ledger(self):
        _, fresh = self.run_export([e(1, "2099-01-01")], as_of="2099-01-10", stale_after=3)
        self.assertEqual((fresh["days_since_latest_entry"], fresh["stale"]), (9, True))
        _, fresh = self.run_export([e(1, "2099-01-09")], as_of="2099-01-10", stale_after=3)
        self.assertFalse(fresh["stale"])

    def test_runs_on_the_synthetic_sample(self):
        s = ROOT / "data" / "sample"
        code = export.main(["--ledger", str(s / "ledger.synthetic.jsonl"), "--catalogue",
                            str(s / "catalogue.synthetic.json"), "--out", str(self.dir / "out"),
                            "--as-of", "2099-01-31"])
        self.assertEqual(code, 0)
        days = json.loads((self.dir / "out" / "daily_totals.json").read_text(encoding="utf-8"))
        self.assertTrue(days)
        self.assertTrue(any(d["nutrients"]["fibre_g"]["value"] is None for d in days))


if __name__ == "__main__":
    unittest.main()
