# What Atlas keeps out of the repository

Atlas is a bookkeeping system for food and biometric data. The code and the documentation are public. Your data is not, and this page says where the line is.

## Never in the repository

- Real food logs, photos or recipes from a person's own life.
- Health values of any kind: weights, lab results, blood pressure, sleep, heart-rate variability, training load, supplement doses.
- Exports from any wearable or health app, and any tokens, client ids or secrets used to reach one.
- Names of people, family details, or anything about a person's health.
- Employer or workplace information.
- File paths that contain a real user name.

## What the repository holds instead

- Documents that describe the design: the data model, the file formats, the confidence labels and the day-quality rule.
- Planned: invented sample data, clearly named as synthetic, generated from a fixed seed so anyone can reproduce it.
- Planned: scripts that read your files from a folder you name, outside the repository.

## How you keep your own data out

1. Keep your ledger, catalogue and exports in a folder that is not inside a clone of this repository.
2. When the scripts land, pass them that folder's paths. They will take paths as arguments and never assume one.
3. Before you commit anything, read the diff once and run a secret scanner over it.
4. If you do find real data in a commit, treat it as leaked: rotate any token, and follow SECURITY.md.

## Why this matters

Atlas never fills a gap with a guess, and it keeps every figure's source label. The same care applies to privacy: the public part describes how the numbers are made, and the numbers themselves stay with the person they belong to.
