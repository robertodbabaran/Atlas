# Testing

The tests use only the Python standard library. No install step.

From the repository root:

    python -m unittest discover -s tests -v

Tested with Python 3.13.

## What the tests protect

The tests exist mainly to hold the rules that make the numbers honest. A refactor that breaks one of these should fail loudly:

- the ledger is append-only: writing a new entry never changes a byte of the existing file
- ids are never reused, and a correction must point at an entry that exists
- the status of an entry is one of exactly four words: label, weighed, estimate, unconfirmed
- an estimate carries a range that contains its amount
- a missing amount is stored as null and read back as null, never as zero

## Test data

Tests build their own small ledgers in a temporary folder, with invented foods and dates in 2099. They never read anything outside the repository. If you add a test, keep to that: no real logs, no real dates, nothing from your own files.

## Planned

Tests for the sample-data generator and for the export will join these as those scripts land, and a CI workflow will run the whole suite on every push.
