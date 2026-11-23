# Estimates and the midpoint rule

Sometimes the person logging cannot give an exact amount, only a range: "between 200 and 300". Atlas has one convention for this so that two people logging the same meal get the same number.

## The rule

1. Set the amount to the midpoint of the stated range. For 200 to 300, that is 250.
2. Set the label to `estimate`.
3. Keep the range in the entry as `range: [200, 300]`.

## Example

```
{"id": "e-000012", "date": "2099-02-03", "slot": "lunch", "food_id": "sample-rice", "amount": 250, "unit": "g", "status": "estimate", "range": [200, 300]}
```

## Why the midpoint

It is simple, it can be reproduced, and it is wrong by at most half the range in either direction. Picking the low end or the high end builds a bias into every total.

## Keeping the range

The range is what lets a later view show uncertainty honestly. A total made of estimates can report a lower and an upper bound by summing the range ends.

## When better information arrives

Add a correction with the new amount and the label `weighed` or `label`, pointing at the estimate. Do not edit the original line. See `docs/CORRECTIONS.md` and `docs/SOURCES_AND_LABELS.md`.

## When there is no range

If the person cannot give even a range, the amount is `null` and the label is `unconfirmed`. Never write a guess as if it were a range.
