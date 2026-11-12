"""Append-only ledger helper for Atlas.

The ledger is a JSON Lines file: one entry per line. This module only ever adds
lines. It never rewrites, reorders or removes one. A correction is a new entry
whose "corrects" field names the entry it replaces; the old line stays.

Rules enforced here:
- status is one of the four confidence labels: label, weighed, estimate, unconfirmed
- an estimate carries a range [low, high] around its amount
- a missing amount is stored as null and stays null; it is never turned into 0
- ids are unique, and a correction must point at an entry that exists
- a line with a "meta" key (for example a synthetic-data note) is not an entry
"""
import json
import re
from pathlib import Path

LABELS = ("label", "weighed", "estimate", "unconfirmed")
UNITS = ("g", "ml", "item")
REQUIRED = ("id", "date", "slot", "food_id", "amount", "unit", "status")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class LedgerError(ValueError):
    pass


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate(entry):
    """Raise LedgerError if the entry breaks a rule. Returns the entry unchanged."""
    if not isinstance(entry, dict):
        raise LedgerError("an entry must be an object")
    missing = [k for k in REQUIRED if k not in entry]
    if missing:
        raise LedgerError(f"missing fields: {', '.join(missing)}")
    if not isinstance(entry["id"], str) or not entry["id"]:
        raise LedgerError("id must be a non-empty string")
    if not isinstance(entry["date"], str) or not DATE_RE.match(entry["date"]):
        raise LedgerError("date must be YYYY-MM-DD")
    if entry["status"] not in LABELS:
        raise LedgerError(f"status must be one of {', '.join(LABELS)}")
    if entry["unit"] not in UNITS:
        raise LedgerError(f"unit must be one of {', '.join(UNITS)}")
    amount = entry["amount"]
    if amount is not None and (not _is_number(amount) or amount < 0):
        raise LedgerError("amount must be a number of zero or more, or null when it is not known")
    if entry["status"] == "estimate" and amount is not None:
        rng = entry.get("range")
        if (not isinstance(rng, list) or len(rng) != 2 or not all(_is_number(x) for x in rng)
                or not rng[0] <= amount <= rng[1]):
            raise LedgerError("an estimate needs a range [low, high] that contains the amount")
    if "corrects" in entry and (not isinstance(entry["corrects"], str) or entry["corrects"] == entry["id"]):
        raise LedgerError("corrects must name another entry's id")
    return entry


def read(path):
    """Return the entries in file order. Meta lines are skipped. A bad line raises with its number."""
    entries = []
    p = Path(path)
    if not p.exists():
        return entries
    with open(p, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise LedgerError(f"line {n}: not valid JSON ({e.msg})") from None
            if isinstance(obj, dict) and "meta" in obj:
                continue
            try:
                validate(obj)
            except LedgerError as e:
                raise LedgerError(f"line {n}: {e}") from None
            entries.append(obj)
    return entries


def append(path, entry):
    """Validate the entry against the rules and the existing file, then add it as one new line."""
    validate(entry)
    existing = read(path)
    ids = {e["id"] for e in existing}
    if entry["id"] in ids:
        raise LedgerError(f"id {entry['id']} is already in the ledger; ids are never reused")
    if "corrects" in entry and entry["corrects"] not in ids:
        raise LedgerError(f"corrects points at {entry['corrects']}, which is not in the ledger")
    line = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    return entry


def current(entries):
    """Entries still in force: anything named by a later correction is left out.
    Corrections can chain (c corrects b corrects a); only the last one counts."""
    replaced = {e["corrects"] for e in entries if "corrects" in e}
    return [e for e in entries if e["id"] not in replaced]
