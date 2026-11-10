# Glossary

Terms as Atlas uses them.

**Ledger.** The append-only list of what was eaten. One entry per line. Entries are never edited; a correction is a new entry.

**Catalogue.** The list of foods with their nutrient values and where each value came from.

**Slot.** A named part of the day, such as breakfast or dinner, defined in the meal slots configuration.

**Confidence label.** How a figure was obtained: label, weighed, estimate or unconfirmed. See `docs/CONFIDENCE_LABELS.md`.

**Weakest-label rule.** A total takes the weakest label among its inputs. One estimate makes the day an estimate day.

**Missing value.** A value that was not recorded. It stays blank and flagged. It is never treated as zero.

**Standing day.** A reusable template for an ordinary day, used to fill a budget to compare against.

**Budget versus actual.** The comparison of a day or a week of logged intake with the budget set for it.

**Completeness.** The share of expected entries that were logged. A day with low completeness gets no colour in the matrix.

**Day-quality matrix.** The 30-day grid that shows how close each day was to your own target range. It is a log summary, not a health verdict.
