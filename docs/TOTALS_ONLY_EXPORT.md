# Totals-only export pattern

A page or chart built from a ledger should receive sums, not entries. The export step reads the ledger and writes a small data file that contains only daily totals and a freshness record.

## What the export writes

- One row per day with the total for each measure.
- For each total, `known_sum` and a count of inputs that were missing.
- A freshness file with the time the export last ran and the newest ledger date it saw.

## What it never writes

- Item names, notes, or free text from the ledger.
- Individual entry ids.
- Any field that was not named in the export's field list.

## Why

A page that never receives item names cannot leak them. The boundary is enforced by the export's field list, not by good intentions in the page code.

## Missing values

If one input to a day's total is missing, the total is `null` and `known_sum` carries the sum of what is known. A missing input is never counted as zero. See `docs/FRESHNESS_BANNER.md` for how a stale or incomplete day is shown.

## Re-running

The export can be run any number of times. It overwrites its own output files and touches nothing else. It never writes to the ledger.
