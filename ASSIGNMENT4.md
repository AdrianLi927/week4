# Assignment 4 — Fill the gaps, and keep the raw file safe

`data/night.csv` is six minutes of the wristband recording from a patient's night, one reading every 15 seconds, in the format you met in the lecture. Six readings were dropped. Before anyone computes anything clinical from it, the ward wants the gaps filled — and a new file saved for the next step of their analysis. The raw file must never be touched.

You will specify two new steps, order their bodies, and prove that they work with pytest.

## Start from

This zip is your **complete starting project**. Everyone starts from exactly these files, so do not mix them with your tutorial folder:

| file | what is in it |
|---|---|
| `vitals.py` | the lecture's `load_recording`, `percent_above` and `make_recording_file`, and, at the bottom, the **signatures** of your two new steps with placeholder `# PROMPT` blocks and `raise NotImplementedError` as their bodies |
| `test_vitals.py` | the lecture's 7 tests, and a marked place for yours |
| `make_fixtures.py` | the lecture's generator script, for your own known-answer files |
| `main.py` | the lecture's orchestrator, which you will change for this assignment |
| `data/` | the lecture's files, plus the new recording `night.csv` |
| `README_template.md` | copy it to `README.md` and fill it in |

Unzip it into a new folder, create the `.venv` there, `python -m pip install pytest`, and check that `python -m pytest` says **7 passed** before you change anything.

## The two steps

Their **names and inputs are fixed**, because your tests will be run automatically. The signatures are already at the bottom of `vitals.py`: do not rename them or change their parameters.

```python
def fill_gaps(readings_bpm: list) -> list:
    ...

def save_recording(path, readings_bpm: list, interval_s: float) -> None:
    ...
```

**`fill_gaps`** takes the list that `load_recording` returns (0 = dropped sample, above 250 bpm = artefact) and returns a **new** list of the same length with the gaps filled. The list passed in must not change.

How to fill a gap is **your decision**, and it changes the answer. Two common rules:

- *carry forward*: a gap takes the last reading before it;
- *linear interpolation*: a gap takes the value on the straight line between the readings on either side.

Whichever you choose, the recording will make you decide more than the rule. What happens to a gap at the very start or the very end? What happens when the reading next to a gap is an artefact? Look at the file before you write the prompt.

**`save_recording`** writes the readings to a **new** file in exactly the wristband format, so that `load_recording` can read it back. It must **refuse** to overwrite a file that already exists, with a `FileExistsError` (lecture: mode `"x"`). You decide how many decimals to write, and how a gap that is still 0 is written.

## What to do

1. **SPECIFY** both steps: a `# PROMPT` block above each signature in `vitals.py`, with every decision in it.
2. **Write the checks before ordering the bodies**, as in the lecture slide *Building the test file, step by step*: in `test_vitals.py`, each new test has a name starting `test_`, a docstring with the expected value and where it came from, and `assert False, "body not written yet"` as its body until the assistant fills it in (a test with an empty body passes and checks nothing). The file keeps its `# PROMPT` block. You need:
   - at least one fixture file **written by hand** in `data/`, with its expected result worked out by hand in the test's docstring;
   - at least one file with a **known answer by construction** (`make_recording_file` already makes recordings without gaps — what should `fill_gaps` do to those?);
   - a **round trip**: save a list, load it back, compare;
   - a test that `save_recording` refuses to overwrite, and leaves the existing file as it was.
3. **Order** the bodies, and the test bodies, in **separate chats**. The test-body chat never sees `vitals.py`.
4. Run `python -m pytest` until it passes, and **read the count**.
5. **Only then**, run `main.py` on `data/night.csv`: print the percentage of valid readings above 100 bpm **before** and **after** filling, and save the filled recording as `data/night_filled.csv`.

`night.csv` is a tidy wristband file, so the `load_recording` you already have reads it, and `save_recording` writes the same tidy format with plain `write`. The `csv` module from the lecture is not needed here — but if your prompt asks for it, that is fine too.

Think about what a careless version of each function could get wrong, and make sure at least one of your tests would notice. Two examples to start you off: a `fill_gaps` that returns a list of a different length; a `fill_gaps` that changes the list you gave it. There are more.

### A new pytest tool: `tmp_path`

A test of `save_recording` needs a file that does not exist yet — and your second run must not fail because the first one left it behind. Put `tmp_path` in the brackets of the test, and pytest hands it a fresh, empty folder of its own:

```python
def test_round_trip(tmp_path):
    """..."""
    path = tmp_path / "out.csv"
    vitals.save_recording(path, [100, 0, 98.3], interval_s=15)
    ...
```

`main.py` is different: run it twice and the second run stops with `FileExistsError`. That is the fence working. Delete `data/night_filled.csv` by hand if you need to run it again.

## Submit (on Moodle, before Monday's lecture)

Your project folder as one zip, **without** `.venv`:

1. `vitals.py` — every function you added with its `# PROMPT` block above it
2. `test_vitals.py` — with its `# PROMPT` block; `python -m pytest` from the project folder must pass
3. `data/` — `night.csv` unchanged, your fixtures (the hand-written one included); not `night_filled.csv`
4. `main.py`
5. `README.md`, from the template
6. the **transcript**

