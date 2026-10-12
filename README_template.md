# Assignment 4 — Fill the gaps

## The rule I chose

<!-- Which rule fills a gap, in one sentence. Then: why this one, for a heart-rate recording? -->

## The edges I decided

| case | what my `fill_gaps` does | why |
|---|---|---|
| a gap at the start of the recording | | |
| a gap at the end of the recording | | |
| two or more gaps in a row | | |
| a gap next to an artefact | | |

## How `save_recording` writes

<!-- Decimals, how a gap that is still 0 is written, what happens if the file exists. -->

## Results on `data/night.csv`

| | % of valid readings above 100 bpm |
|---|---|
| before filling | |
| after filling | |

<!-- Two or three sentences: why did the number change (or not)? Would a clinician reading only the "after" number be misled? -->

## What the assistant decided that I had not

<!-- Look at the end of its replies, and at the code. Be honest: this section is marked for honesty, not for having nothing in it. -->

## My tests, one line each

| test | what it checks | where the expected value came from |
|---|---|---|
| | | |

## The count

<!-- Paste the last line of `python -m pytest`, e.g. "9 passed in 0.03s". -->
