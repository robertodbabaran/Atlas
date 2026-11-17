"""Make Atlas's invented sample data.

Everything this script writes is synthetic. The foods are made up, the nutrient
values are round invented numbers (not reference data), and the dates sit in
2099 so nobody mistakes them for a real diary. The same seed always gives the
same bytes, so the sample files can be checked in CI.

    python scripts/make_sample.py                 write data/sample/
    python scripts/make_sample.py --check         exit 1 if data/sample/ differs from a fresh run

The ledger deliberately includes the awkward cases the rules are about:
estimates with ranges, unconfirmed entries, an amount that was never recorded
(null, not zero), a food with one nutrient missing, corrections that supersede
an earlier line, and days with nothing logged at all.
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
import random

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger  # noqa: E402

NOTE = ("SYNTHETIC. Invented for testing Atlas. Not real food, not real nutrient data, "
        "not a real person's log.")
SLOTS = ("breakfast", "lunch", "dinner", "snack")

# Invented foods. Values are round made-up numbers per basis, chosen only to look plausible.
FOODS = [
    {"food_id": "sample-grain-bowl", "name": "Sample grain bowl", "per": "100 g",
     "nutrients": {"energy_kcal": 150, "protein_g": 5.0, "fibre_g": 3.0, "sodium_mg": 120}},
    {"food_id": "sample-bean-stew", "name": "Sample bean stew", "per": "100 g",
     "nutrients": {"energy_kcal": 110, "protein_g": 7.0, "fibre_g": 6.0, "sodium_mg": 300}},
    {"food_id": "sample-green-salad", "name": "Sample green salad", "per": "100 g",
     "nutrients": {"energy_kcal": 40, "protein_g": 2.0, "fibre_g": 2.5, "sodium_mg": 60}},
    {"food_id": "sample-fish-fillet", "name": "Sample fish fillet", "per": "100 g",
     "nutrients": {"energy_kcal": 160, "protein_g": 22.0, "fibre_g": 0.0, "sodium_mg": 90}},
    {"food_id": "sample-yogurt-cup", "name": "Sample yogurt cup", "per": "1 item",
     "nutrients": {"energy_kcal": 120, "protein_g": 10.0, "fibre_g": 0.0, "sodium_mg": 70}},
    {"food_id": "sample-fruit", "name": "Sample fruit", "per": "1 item",
     "nutrients": {"energy_kcal": 90, "protein_g": 1.0, "fibre_g": 3.0, "sodium_mg": 0}},
    {"food_id": "sample-snack-bar", "name": "Sample snack bar", "per": "1 item",
     "nutrients": {"energy_kcal": 200, "protein_g": 8.0, "fibre_g": None, "sodium_mg": 150}},
]
UNIT = {f["food_id"]: ("item" if f["per"] == "1 item" else "g") for f in FOODS}


def _pick(rng, seq):
    return seq[int(rng.random() * len(seq))]


def build(seed=7, start="2099-01-01", days=30):
    rng = random.Random(seed)
    d0 = date.fromisoformat(start)
    entries, n = [], 0
    weighed_ids = []
    for i in range(days):
        day = (d0 + timedelta(days=i)).isoformat()
        if rng.random() < 0.1:
            continue  # nothing logged that day: the day is absent, not zero
        for slot in SLOTS:
            if slot == "snack" and rng.random() < 0.5:
                continue
            food = _pick(rng, FOODS)["food_id"]
            unit = UNIT[food]
            amount = 1 if unit == "item" else 50 + 10 * int(rng.random() * 26)
            r = rng.random()
            status = "weighed" if r < 0.45 else "label" if r < 0.65 else "estimate" if r < 0.9 else "unconfirmed"
            if unit == "item" and status == "weighed":
                status = "label"
            n += 1
            e = {"id": f"e-{n:06d}", "date": day, "slot": slot, "food_id": food,
                 "amount": amount, "unit": unit, "status": status}
            if status == "estimate":
                spread = 0.2 * amount
                e["range"] = [round(amount - spread, 1), round(amount + spread, 1)]
            if status == "unconfirmed" and rng.random() < 0.5:
                e["amount"] = None
                e["note"] = "amount not recorded"
            if status == "weighed":
                weighed_ids.append(e)
            entries.append(ledger.validate(e))
    # three later corrections: new lines that supersede an earlier weighed entry
    for k in range(3):
        old = weighed_ids[int(rng.random() * len(weighed_ids))]
        if any(e.get("corrects") == old["id"] for e in entries):
            continue
        n += 1
        fixed = dict(old, id=f"e-{n:06d}", amount=old["amount"] - 20 if old["amount"] > 60 else old["amount"] + 20,
                     corrects=old["id"], note="re-weighed; replaces the earlier line")
        entries.append(ledger.validate(fixed))
    return entries


def render(entries):
    cat = {"_data": "SYNTHETIC", "meta": "synthetic", "note": NOTE, "foods": [
        dict(f, source="invented for the Atlas sample", source_status="estimate") for f in FOODS]}
    cat_text = json.dumps(cat, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    lines = [json.dumps({"_data": "SYNTHETIC", "meta": "synthetic", "note": NOTE}, sort_keys=True)]
    lines += [json.dumps(e, sort_keys=True, ensure_ascii=False) for e in entries]
    return {"catalogue.synthetic.json": cat_text, "ledger.synthetic.jsonl": "\n".join(lines) + "\n"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "data" / "sample"))
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--check", action="store_true", help="compare with the files on disk; write nothing")
    a = ap.parse_args(argv)
    files = render(build(seed=a.seed))
    out = Path(a.out)
    if a.check:
        bad = [name for name, text in files.items()
               if not (out / name).exists() or (out / name).read_bytes().replace(b"\r\n", b"\n") != text.encode("utf-8")]
        print("sample data matches a fresh run" if not bad else "differs: " + ", ".join(bad))
        return 1 if bad else 0
    out.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        with open(out / name, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("wrote", out / name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
