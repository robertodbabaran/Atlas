# Sample data policy

Atlas ships sample data so the views and the matrix can be run and tested. Sample data in this repository is invented or heavily transformed. It describes no real person.

## How sample data is made

1. A small generator script creates a 30-day ledger from fixed random seeds, so results are reproducible.
2. Foods, amounts and dates are fictional. Dates are in a clearly fictional range.
3. Biometric sample rows are generated from simple distributions, with day-to-day correlation, and rounded.
4. Every sample file is labelled as synthetic in its name and in a note at the top.

## Checks before a sample file is published

- No row matches or nearly matches any real record.
- No real date, name, place, device identifier or account identifier appears.
- Values are rounded so exact real figures cannot be recovered.
- The file passes the repository's secret and personal-data scan.
- A person reads the file once before it is added.

## What does not belong here

Real food logs, photos, health values, device exports, tokens or credentials. Anyone running Atlas on their own data keeps that data outside the repository.
