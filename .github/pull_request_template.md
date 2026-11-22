## What this changes

## Why

## Checks

- [ ] `python -m unittest discover -s tests` passes
- [ ] If the sample generator changed, `python scripts/make_sample.py` was re-run and the new sample files are in this change
- [ ] Missing values still stay missing (null, never zero) and every figure keeps its label
- [ ] No real data: no food logs, photos, health values, device exports, names, or paths with a user name
