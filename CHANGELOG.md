# Changelog

Notable changes to Atlas. The format follows Keep a Changelog. Nothing has been released yet, so everything is under Unreleased.

## Unreleased

### Added

Design documents
- Data model (`docs/DATA_MODEL.md`) and architecture overview (`docs/ARCHITECTURE.md`).
- Device-neutral biometrics schema proposal (`docs/SOURCE_SCHEMA.md`).
- Confidence labels, with the rule that a total inherits its weakest label (`docs/CONFIDENCE_LABELS.md`), and a practical guide to choosing one (`docs/SOURCES_AND_LABELS.md`).
- File format examples (`docs/FILE_FORMATS.md`).
- Corrections as new lines that supersede old ones (`docs/CORRECTIONS.md`).
- Freshness banner design (`docs/FRESHNESS_BANNER.md`).
- Day-quality rule for the 30-day matrix (`docs/DAY_QUALITY_RULE.md`).
- Sample data policy (`docs/SAMPLE_DATA.md`), privacy boundary (`docs/PRIVACY_BOUNDARY.md`), glossary (`docs/GLOSSARY.md`), knowledge entry template (`docs/KNOWLEDGE_ENTRY_TEMPLATE.md`), roadmap (`docs/ROADMAP.md`) and how to run the tests (`docs/TESTING.md`).

Configuration
- Meal slots (`config/meal_slots.json`).
- Targets example with placeholders only; Atlas ships no default targets (`config/targets.example.json`).

Code
- Append-only ledger helper (`scripts/ledger.py`).
- Sample data generator (`scripts/make_sample.py`) and its synthetic output (`data/sample/`).
- Export of daily totals and a freshness file (`scripts/export.py`).
- Tests for all three (`tests/`), run by a CI workflow on every push (`.github/workflows/ci.yml`).

Repository
- Bug report and feature request issue templates.

### Not built yet
The 7-day and 30-day views and the 30-day matrix. No licence has been chosen, and no version has been tagged.
