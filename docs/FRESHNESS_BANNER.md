# Freshness banner

Status: design. The export that produces it is planned for v0.1.

A view built from old data looks exactly like a view built from today's data. The freshness banner is there so it does not. Every generated view opens with one line that says how current its inputs are, and turns into a warning when they are not.

Examples of what the line says (invented dates):

    Data through 2099-01-30, one day before this view was built. 5 days in the span have no entries.
    STALE: the newest entry is 9 days old (limit 3). Totals below stop at 2099-01-01.

## Where the numbers come from

The export writes a small freshness file next to the daily totals. It records:

- the date the export was run for
- the date of the newest ledger entry, and how many days old it is
- the limit, in days, after which the data counts as stale (you set it; the export takes it as an option)
- the days inside the logged span that have no entries at all
- a hash of each input file, so a view can be traced to the exact ledger and catalogue it came from

Views read that file. They never work out freshness on their own, so every view agrees.

## Rules

- A stale source is shown, not hidden. The view still renders, with the warning at the top, because old data plainly labelled is more useful than a blank page.
- Days with nothing logged are listed, not filled. A gap in logging is not a day of eating nothing.
- The banner reports on the data. It does not nag about logging habits.
