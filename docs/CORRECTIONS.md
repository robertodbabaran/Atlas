# Corrections and superseding

Atlas never edits a ledger line once it is written. When an entry turns out to be wrong, you add a new line that says which line it replaces. The old line stays in the file.

## Why not just fix the line

A ledger that can be edited in place cannot be audited. If yesterday's 250 g silently becomes 200 g, nobody reading the file later can tell that the first figure existed, or why it changed. Accountants solved this long ago with reversing entries. Atlas borrows the idea in its simplest form.

It also keeps the file easy to diff and back up: every change to the ledger is an added line at the end, never a change in the middle.

## How it looks

```
{"id": "e-000041", "date": "2099-01-12", "slot": "dinner", "food_id": "sample-bean-stew", "amount": 300, "unit": "g", "status": "estimate", "range": [240, 360]}
{"id": "e-000057", "date": "2099-01-12", "slot": "dinner", "food_id": "sample-bean-stew", "amount": 280, "unit": "g", "status": "weighed", "corrects": "e-000041", "note": "weighed the leftovers"}
```

The second line supersedes the first. Totals for 12 January use 280 g and the label `weighed`. The estimate is still in the file for anyone who wants to see what was believed before.

## Rules

1. A correction is a complete entry, not a patch. It repeats every field, with the fixed values.
2. `corrects` names the id of the entry it replaces. That id must already exist.
3. Ids are never reused, so a correction always gets a new one.
4. Corrections can chain. If c corrects b and b corrects a, only c counts.
5. If the same meal was logged twice, correct the duplicate with an amount of 0 and say so in `note`. If the true amount is unknown, the correction uses `null` and the label `unconfirmed`. Zero is only for food that really was not eaten, never a stand-in for "not sure".
6. Views and totals read only the entries still in force. Nothing generated from the ledger is edited by hand to "fix" a number.

## When a better source arrives

A common correction is not a wrong amount but a better label: you estimated a portion, then found the package and read the label. That is the same mechanism. The new line carries `status: "label"` and points at the estimate. See `docs/SOURCES_AND_LABELS.md` for how the label on a figure is chosen.
