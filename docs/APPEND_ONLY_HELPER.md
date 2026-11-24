# Append-only helper pattern

Any script that adds lines to a ledger should follow four habits. `scripts/ledger.py` is the reference implementation.

1. **Backup first.** Before the first write in a run, copy the file to a dated backup beside it. If the copy fails, stop.
2. **Dry run.** A `--dry-run` flag prints the lines that would be added and exits without writing. Use it whenever you are unsure.
3. **Append only.** The helper opens the file in append mode. It has no code path that rewrites or deletes a line.
4. **Validate before writing.** Labels must be one of the four allowed values. A missing amount stays `null`. A correction must name an id that exists.

## Why a dry-run flag matters

The most common mistake in logging is a typo in a unit or date. A dry run shows the line exactly as it will be stored, so the typo is caught before it is permanent.

## Next-due dates

A helper may store a next-due date for a recurring item. The rule is simple: the next date is computed from the last logged date plus the interval, never from today. Logging late does not shift the schedule.

## What the helper does not do

It does not edit past lines, merge duplicates, or guess missing values. Those are corrections, and corrections are new lines. See `docs/CORRECTIONS.md`.
