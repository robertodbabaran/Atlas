# Architecture

Status: design. Items marked planned are not built yet.

    ledger.jsonl --------\
    catalogue.json ------+--> export --> daily totals --> views (7-day, 30-day, matrix)
    standing_day.json ---/                                   ^
                                                             |
    biometrics (device-neutral daily table) -----------------+   (optional, planned)

## Parts

- **Ledger:** an append-only log, one line per entry. Corrections are new entries that point at the one they replace.
- **Catalogue:** foods and their nutrient values, each with a source.
- **Standing day:** the daily budget: energy, macronutrients and a short list of micronutrients, with floors, ceilings and ranges.
- **Export:** a script that reads the three files above and writes daily totals, carrying the weakest confidence label of the inputs.
- **Views:** static pages generated from the export. They are never edited by hand.
- **Biometrics link (planned):** adapters map a device's export into a device-neutral daily table, which feeds views that show intake next to sleep and recovery.

## Design choices

- Plain files, so every change is a readable diff.
- One direction of data flow. Views are outputs.
- No real data in the repository.
- Every number carries a confidence label. Missing stays missing.
