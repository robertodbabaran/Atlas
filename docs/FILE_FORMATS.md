# File formats

Status: design. All example lines are invented. The shapes may change before v0.1.0.

Atlas uses plain files. Each one can be read, diffed and backed up.

## Ledger (JSON Lines, append-only)

One entry per line. An entry is never edited. A correction is a new entry with a `corrects` field.

```
{"id": "e-000001", "date": "2026-01-14", "slot": "lunch", "food_id": "lentils-cooked", "amount": 250, "unit": "g", "status": "weighed"}
{"id": "e-000002", "date": "2026-01-14", "slot": "dinner", "food_id": "yogurt-plain", "amount": 1, "unit": "item", "status": "estimate", "range": [0.8, 1.2]}
{"id": "e-000003", "date": "2026-01-14", "slot": "lunch", "food_id": "lentils-cooked", "amount": 200, "unit": "g", "status": "weighed", "corrects": "e-000001"}
```

## Catalogue (JSON)

One record per food. Every nutrient value says where it came from.

```
{"food_id": "lentils-cooked", "name": "Lentils, cooked", "per": "100 g",
 "nutrients": {"energy_kcal": 116, "protein_g": 9.0, "fibre_g": 7.9},
 "source": "example database, record 0000", "source_status": "database"}
```

## Standing day (JSON)

The daily budget. Each nutrient has a kind (floor, ceiling or range), a target, and where the target came from.

```
{"energy_kcal": {"kind": "range", "low": 2000, "high": 2200, "source": "personal choice"},
 "fibre_g": {"kind": "floor", "target": 25, "source": "example reference"},
 "sodium_mg": {"kind": "ceiling", "limit": 2300, "source": "example reference"}}
```

## Generated files

The export writes daily totals and a freshness file. Views read only the export and are never edited by hand.
