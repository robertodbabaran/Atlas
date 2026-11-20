"""Export daily totals from an Atlas ledger and catalogue.

    python scripts/export.py --ledger data/sample/ledger.synthetic.jsonl \
        --catalogue data/sample/catalogue.synthetic.json --out out/ --as-of 2099-01-31

Writes two files into --out:
  daily_totals.json  one record per day that has entries
  freshness.json     how old the newest entry is, which days in the span have nothing, input hashes

Rules:
- Only entries still in force count (a corrected line is replaced by its correction).
- A nutrient total is null when any input to it is missing (amount not recorded, food not in
  the catalogue, nutrient value blank, or a unit that does not match the catalogue basis).
  The sum of the inputs that are known is reported beside it as known_sum, never as the total.
- A day with no entries is not written as zero. It is absent from daily_totals.json and listed
  in freshness.json.
- Each day carries the weakest confidence label among its entries. Strongest to weakest, in the
  order the labels are published: label, weighed, estimate, unconfirmed.
- low and high carry estimate ranges through; for other labels they equal the value.
"""
import argparse
import hashlib
import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger  # noqa: E402

ORDER = ("label", "weighed", "estimate", "unconfirmed")  # strongest first


def weakest(labels):
    labels = list(labels)
    if not labels:
        return None
    return max(labels, key=ORDER.index)


def load_catalogue(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    foods = data["foods"] if isinstance(data, dict) else data
    return {f["food_id"]: f for f in foods}


def _factor(entry, food):
    """How many catalogue bases the entry amount represents, or None if it cannot be worked out."""
    per = food.get("per", "").split()
    if len(per) != 2:
        return None
    try:
        base = float(per[0])
    except ValueError:
        return None
    unit = {"g": "g", "ml": "ml", "item": "item"}.get(per[1])
    if unit != entry["unit"] or base <= 0:
        return None
    return 1.0 / base


def day_totals(entries, catalogue):
    nutrients = sorted({k for f in catalogue.values() for k in f.get("nutrients", {})})
    acc = {k: {"value": 0.0, "low": 0.0, "high": 0.0, "missing_inputs": 0} for k in nutrients}
    for e in entries:
        food = catalogue.get(e["food_id"])
        factor = _factor(e, food) if food else None
        amt = e["amount"]
        lo, hi = (e["range"] if e["status"] == "estimate" and amt is not None else (amt, amt))
        for k in nutrients:
            per = food.get("nutrients", {}).get(k) if food else None
            if amt is None or factor is None or per is None:
                acc[k]["missing_inputs"] += 1
                continue
            acc[k]["value"] += amt * factor * per
            acc[k]["low"] += lo * factor * per
            acc[k]["high"] += hi * factor * per
    out = {}
    for k, a in acc.items():
        if a["missing_inputs"]:
            out[k] = {"value": None, "low": None, "high": None,
                      "known_sum": round(a["value"], 1), "missing_inputs": a["missing_inputs"]}
        else:
            out[k] = {"value": round(a["value"], 1), "low": round(a["low"], 1),
                      "high": round(a["high"], 1), "missing_inputs": 0}
    return out


def export(ledger_path, catalogue_path, as_of, stale_after=3):
    entries = ledger.current(ledger.read(ledger_path))
    catalogue = load_catalogue(catalogue_path)
    by_day = {}
    for e in entries:
        by_day.setdefault(e["date"], []).append(e)
    days = []
    for d in sorted(by_day):
        es = by_day[d]
        days.append({"date": d, "entries": len(es), "label": weakest(e["status"] for e in es),
                     "nutrients": day_totals(es, catalogue)})
    as_of_d = date.fromisoformat(as_of)
    latest = max(by_day) if by_day else None
    gaps = []
    if by_day:
        d, end = date.fromisoformat(min(by_day)), date.fromisoformat(latest)
        while d <= end:
            if d.isoformat() not in by_day:
                gaps.append(d.isoformat())
            d += timedelta(days=1)
    age = (as_of_d - date.fromisoformat(latest)).days if latest else None
    fresh = {
        "as_of": as_of,
        "latest_entry_date": latest,
        "days_since_latest_entry": age,
        "stale_after_days": stale_after,
        "stale": True if age is None else age > stale_after,
        "days_with_entries": len(by_day),
        "days_without_entries": gaps,
        "inputs": {name: hashlib.sha256(Path(p).read_bytes()).hexdigest()
                   for name, p in (("ledger", ledger_path), ("catalogue", catalogue_path))},
    }
    return days, fresh


def _write(path, obj):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Export daily totals from an Atlas ledger.")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--catalogue", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--as-of", required=True, help="the date the export is run for, YYYY-MM-DD")
    ap.add_argument("--stale-after", type=int, default=3, help="days without a new entry before the data counts as stale")
    a = ap.parse_args(argv)
    days, fresh = export(a.ledger, a.catalogue, a.as_of, a.stale_after)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    _write(out / "daily_totals.json", days)
    _write(out / "freshness.json", fresh)
    flag = "STALE" if fresh["stale"] else "fresh"
    print(f"{len(days)} days exported; latest entry {fresh['latest_entry_date']}; {flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
