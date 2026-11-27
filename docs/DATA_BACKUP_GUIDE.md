# Backing up your ledger

The ledger is a plain text file, so backups are simple. The point is to have more than one copy and to know that each is readable.

## Habits

1. Keep at least two copies, on different devices.
2. Copy, never move. The working file stays where it is.
3. Name backups with the date: `ledger-2099-03-01.jsonl`.
4. Never overwrite an earlier backup. A bad edit would then be copied over the good file.
5. Once a month, open one backup and read the last ten lines.

## Why append-only helps

Because lines are only ever added, an older backup is always a prefix of a newer file. If the two differ in the middle, something edited the file by hand, and you know to investigate.

## What to keep out of public places

The ledger itself. Share totals or synthetic data, never the file. See `docs/PRIVACY_BOUNDARY.md` and `docs/TOTALS_ONLY_EXPORT.md`.

## Restoring

Copy the newest backup over the working file only after checking that the working file is damaged. Keep the damaged file under another name.
