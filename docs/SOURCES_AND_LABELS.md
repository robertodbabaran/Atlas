# Sources and labels: choosing the label for a figure

`docs/CONFIDENCE_LABELS.md` defines the four labels. This page is the practical side: when you log something, which label does it get, and what changes it later.

Ask two questions about the entry.

**How do you know the amount?** If you put it on a scale, it is `weighed`. If the package says it holds one 150 g portion and you ate the whole thing, the amount comes from the label. If you judged it by eye or from a photo, it is an `estimate` and you record a range. If you typed a number without any check, it is `unconfirmed`.

**How do you know what is in it?** That is the catalogue's job, not the entry's. Every catalogue record names its source: a package label, a reference database record, or an estimate. A catalogue figure marked estimate is a prompt to find a better source.

## Worked examples (invented)

- A cup of plain yogurt, nutrition panel read off the lid, eaten whole: `label`.
- Cooked rice, scooped onto a scale: `weighed`.
- A restaurant curry, judged at about 350 g, somewhere between 280 and 420: `estimate`, with `range: [280, 420]`.
- "Had a snack around four", amount not remembered: `unconfirmed`, and the amount stays `null`. It is not entered as a typical portion.

## An estimate is never promoted by editing

When you later find the package, weigh the leftovers, or learn the recipe, the figure gets better. Atlas records that as a new ledger line that replaces the old one, carrying the stronger label. The estimate stays in the file. The same goes for the catalogue: when a label-sourced value replaces an estimated one, the record's source changes and any "label needed" flag on it clears.

## What a label is not

A label says how a figure was obtained. It does not say whether the food was a good choice, and it does not make a figure more or less important. A weighed portion of something you rarely eat counts the same as any other weighed portion.

## Totals

A total takes the weakest label among its inputs. One `unconfirmed` entry makes the whole day `unconfirmed`. That can feel harsh, but it is the honest reading: the total is only as solid as its least certain part. For this rule Atlas ranks the labels in the order `docs/CONFIDENCE_LABELS.md` lists them, strongest first: label, weighed, estimate, unconfirmed.
