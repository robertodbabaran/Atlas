# Data model

Status: design. Nothing here is built yet. All examples use invented values.

Atlas keeps health data the way a bookkeeper keeps money: an append-only ledger, a catalogue that defines the things in it, a budget, and reports that compare budget to actual.

## 1. Ledger

One line per entry, in a JSONL file. Entries are only ever added, never edited. A correction is a new entry that points at the one it replaces.

| Field | Meaning | Example |
|---|---|---|
| `id` | Unique, never reused | `e-000123` |
| `date` | Day the entry belongs to (YYYY-MM-DD) | `2026-01-14` |
| `slot` | Meal slot from the config | `lunch` |
| `food_id` | Key into the catalogue | `lentils-cooked` |
| `amount` | A number | `250` |
| `unit` | `g`, `ml` or `item` | `g` |
| `status` | How sure the figure is (see section 5) | `weighed` |
| `corrects` | Optional: `id` of the entry this replaces | `e-000119` |
| `note` | Optional free text | `restaurant, estimated` |

## 2. Catalogue

One record per food. Each nutrient value carries its source, so a reader can check it.

| Field | Meaning | Example |
|---|---|---|
| `food_id` | Unique key | `lentils-cooked` |
| `name` | Human name | `Lentils, cooked` |
| `per` | Basis of the values | `100 g` |
| `nutrients` | Map of nutrient to value and unit | `{"energy_kcal": 116, "protein_g": 9.0}` |
| `source` | Where the values came from | `reference database name and record id` |
| `source_status` | `label`, `database` or `estimate` | `database` |

## 3. Standing day (the budget)

The target for a normal day: energy, macronutrients and a short list of micronutrients, each with a minimum, a target and a maximum where that makes sense. Each target has a source, or is marked as a personal choice.

## 4. Views

Views are generated from the ledger, the catalogue and the standing day. They are never edited by hand.
- Daily totals: sum of amount times the catalogue values, per nutrient, per day.
- 7-day and 30-day views: actual versus the standing day, for macros and micronutrients.
- 30-day matrix: one square per day, green, yellow or red by how close the day came to the standing day. The thresholds are documented with the view.

## 5. Status on every figure

Every number shown carries one of four labels:
- `label`: read from a package label
- `weighed`: measured on a scale
- `estimate`: judged by eye or from a photo, with a range
- `unconfirmed`: entered without a check

A total inherits the weakest label among its inputs. A missing value stays blank and is flagged. Atlas never fills a gap with a guess.

## 6. Biometrics link (optional, later)

A device-neutral table of daily measurements: sleep duration and stages, recovery or readiness score, strain or activity load, resting heart rate, heart-rate variability. A source adapter maps one device's export into this table. The table feeds views that show intake next to sleep and recovery. See the roadmap for when this lands.

## 7. Files

Plain files, readable and diffable: `ledger.jsonl`, `catalogue.json`, `standing_day.json`, and generated `views/`. Real data lives outside this repository. Only invented sample data lives under `data/sample/`.
