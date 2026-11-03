# Atlas

A single ledger reconciling biometric and consumption data, and visualizing health.

> **Status: early.** The repository was created on 2026-11-02. This README describes the design and what is planned. Items marked *planned* are not built yet. The first tagged release (v0.1.0) targets 2026-11-22.

## The idea

Finance has bookkeeping: every transaction goes into a ledger, a catalogue defines what things are, a budget says what should happen, and reports compare budget to actual. Wearables such as WHOOP track exercise, sleep and recovery. Almost nothing tracks food with the same discipline.

Atlas applies bookkeeping to health. Food is logged like transactions, checked against a standing daily budget, and reconciled with biometric data so the two can be read together.

## What it does (design)

| Piece | Role | Status |
|---|---|---|
| Ledger | Append-only log of what was eaten, with a confidence label on every figure (label, weighed, estimate, unconfirmed) | planned |
| Catalogue | Known foods and their nutrient values, each with a source | planned |
| Standing day | The daily budget: calories, macros and micronutrients | planned |
| Views | 7-day and 30-day budget-versus-actual for macros and micronutrients | planned |
| 30-day matrix | A contribution-graph-style grid: green, yellow or red per day | planned |
| Knowledge base | Cited notes on what is healthy and why | planned |
| WHOOP link | Optional module that reads your own WHOOP data (sleep, recovery, strain) next to the food ledger | planned |

## How it is built (design)

- **Plain files.** The ledger and catalogue are JSON and JSONL. They are readable, diffable and easy to back up.
- **One direction of data.** Source files feed one export step. Views are generated from the export and never edited by hand.
- **Every figure carries its status.** The system never fills a gap with a guess. A missing value stays blank and flagged.
- **Python scripts.** One script exports, one builds the views.

Planned layout:

```
Atlas/
README.md LICENSE DISCLAIMER.md SECURITY.md CONTRIBUTING.md
docs/ data model, data map, data flow
knowledge/ cited entries
config/ meal slots, nutrient references, WHOOP settings template
data/sample/ invented sample data
scripts/ export, build views, WHOOP link
views/ generated pages built from sample data
```

## Data and privacy

- This repository contains **synthetic sample data only**. No real food logs, photos, health values or WHOOP data are, or will be, committed.
- If you run Atlas on your own data, keep it outside the repository.
- Secrets such as WHOOP credentials belong in a local file that is git-ignored. Never commit them.

## WHOOP

Atlas is an independent project. It is **not affiliated with, endorsed by or sponsored by WHOOP**. WHOOP is a trademark of its owner. The optional WHOOP link, when built, will use your own registered WHOOP app and your own data. Read WHOOP's developer terms before using it.

## Data sources

Food data will come from sources that allow reuse, each credited where used:
- USDA FoodData Central
- Canadian Nutrient File (Health Canada)
- Open Food Facts (ODbL), queried at runtime, not copied into this repository

## Not medical advice

Atlas is a bookkeeping and visualization tool. It does not provide medical, dietary or nutritional advice. Talk to a qualified clinician before changing your diet, especially if you take medication.

## Roadmap

- **v0.1.0 (target 2026-11-22):** sample data, export script, one 7-day view, the 30-day matrix
- **Next:** tests, continuous integration, the WHOOP link, first cited knowledge entries
- **Later:** a documentation page and a second release

## Licence

No licence has been chosen yet, so all rights are reserved for now. A licence will be added before v0.1.0.

## Author

Roberto Babaran, Toronto
