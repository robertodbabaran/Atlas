# Device-neutral biometrics schema (proposal)

Status: proposal for v0.1. Nothing here is built yet. All values in examples are invented.

Atlas should not depend on one device. This page defines a small daily table that any wearable export can be mapped into, and what a mapping file must declare. It is a design proposal and has not been validated against every vendor's current documentation.

## Rules

1. **Store what was measured and say who measured it.** One row per person per local date per source. Rows from different sources are never merged or averaged.
2. **Zero often means no reading.** For heart-rate variability, resting heart rate, blood-oxygen, temperature and respiratory rate, a stored zero is treated as missing. Steps and energy stay at zero only when wear time confirms the device was worn.
3. **Never impute silently.** A missing value is stored as null with a reason: not_worn, not_scored, sync_failed or implausible.
4. **Sleep belongs to the wake-up date.** Store the UTC offset with each night so day boundaries are reproducible.
5. **Heart-rate variability is only comparable with itself.** Store the value with its method (RMSSD or SDNN) and window (night average, deep sleep, spot). Never convert between methods and never compare across sources.
6. **Scores are proprietary.** Recovery, readiness, sleep and strain scores are stored with the source and, where known, an algorithm version. They are never averaged across brands. Prefer the raw components for analysis.

## Daily table

| Field | Unit | Missing rule |
|---|---|---|
| local_date | ISO date | required |
| source | text | required |
| tz_offset_min | minutes | null if unknown |
| time_in_bed_min | minutes | null |
| time_asleep_min | minutes | zero means missing |
| sleep_deep_min, sleep_rem_min | minutes | zero means missing |
| stage_scheme | text | null |
| hrv_ms | milliseconds | zero or out of range means null |
| hrv_method | rmssd or sdnn | required when hrv_ms is set |
| hrv_window | night_avg, deep_sleep or spot | required when hrv_ms is set |
| rhr_bpm | beats per minute | zero means missing |
| steps | count | null if not worn |
| active_kcal, total_kcal | kilocalories | null if not worn |
| workout_count, workout_min | count, minutes | null |
| wear_minutes | minutes | null |
| score_* | source scale | null; always labelled with source |
| missing_reason | enum | null |

Ranges and field names above are proposals, to be tuned against real exports.

## What a mapping file must declare

1. The source id and the export or API version it targets.
2. For every output field: the source field path, the unit conversion and any transform.
3. For heart-rate variability: method, window and aggregation.
4. The rule that derives local_date and where the UTC offset comes from.
5. The sleep-stage map and the stage_scheme it implies.
6. The missing-value rules per field: sentinel values and the reason code.
7. Score fields: vendor name, scale and version.
8. A fixture with a sample input and the expected output row.
9. Unsupported fields, listed as unsupported and never defaulted to zero.

## Analysis cautions

Comparing food intake with next-day sleep or recovery for one person is exploratory. Daily series are autocorrelated, many comparisons produce false positives, and association is not cause. Atlas shows associations with their sample size and does not claim causes.
