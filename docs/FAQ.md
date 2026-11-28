# Frequently asked questions

**Is this a medical tool?** No. Atlas is bookkeeping. It records what you report and shows how sure each figure is. See `DISCLAIMER.md`.

**Does it contain real personal data?** The public repository contains only invented sample data, with dates in the year 2099 and a label saying "synthetic".

**Why are some amounts empty?** A missing amount stays missing. Filling it with zero would make totals look more certain than they are.

**Why can't I edit a past entry?** The ledger is append-only. You add a correction that points at the old line. See `docs/CORRECTIONS.md`.

**What do the four labels mean?** `label`, `weighed`, `estimate` and `unconfirmed`, from most to least certain. See `docs/CONFIDENCE_LABELS.md`.

**How are estimates made when I only know a range?** Midpoint of the range, labelled `estimate`, with the range kept. See `docs/ESTIMATE_MIDPOINT_RULE.md`.

**Can I use the scripts on my own data?** Yes, locally. Keep your own data out of any public fork. See `docs/PRIVACY_BOUNDARY.md`.

**How do I report a problem?** Open an issue with the bug report template.
