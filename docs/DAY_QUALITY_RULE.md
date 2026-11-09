# Day-quality rule for the 30-day matrix (v0.1)

Status: design. v0.1 uses the simplest rule that is honest. A fuller version is planned for later and is described at the end.

## The v0.1 rule

Each day gets one of four states, and the matrix shows one cell per day with a glyph inside it, so colour is never the only signal.

- **On target (green):** energy is inside your range and protein is at or above your floor.
- **Partly on target (yellow):** exactly one of the two is met.
- **Off target (red):** neither is met.
- **Not enough data (grey):** too few entries were logged to judge the day. Atlas never colours a day it cannot support.

## You set the numbers

Atlas ships with no default targets. You give it an energy range, a protein floor and a minimum share of expected entries that must be logged. Whatever you set is printed under the matrix, so a reader can always see how a colour was decided.

## How the inputs are treated

- Energy and protein come only from logged entries. A missing value stays blank and is never counted as zero.
- A day takes the weakest confidence label among its entries (label, weighed, estimate, or unconfirmed). A day built partly from estimates is shown as an estimate day, and its range is carried through.
- If the lower and upper bound of an incomplete day fall on different sides of your range or floor, the day is grey.

## Cautions

- The matrix reports closeness to your own targets. It is not a health verdict or a diagnosis.
- One day outside your range is a data point, not a failing. Look at the weeks.

## Later

A fuller rule would add floors for nutrients such as fibre and potassium and ceilings for sodium and added sugar. It will need reference values checked against official tables first, so it is not part of v0.1.
