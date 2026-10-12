"""Steps for heart-rate recordings. Definitions only: importing this file prints nothing."""


# PROMPT (final version used):
# Write a Python function load_recording(path) that reads a heart-rate file
# exported by the wearable. Lines starting with '#' are notes from the device
# and are skipped. The first other line is the header 'time_s,hr_bpm'.
# Every line after it is a time in seconds and a heart rate in bpm,
# separated by a comma. An empty heart rate means a dropped sample:
# return it as 0, because that is what percent_above expects.
# Return the heart rates as a list of floats, in file order.
# Open the file with encoding="utf-8". If the file does not exist, let the
# FileNotFoundError happen. Type hints and a docstring stating the units.
# Plain Python, no packages.
def load_recording(path) -> list[float]:
    """Load heart rates (bpm) from a wearable export file.

    Lines starting with '#' are skipped, as is the 'time_s,hr_bpm' header.
    An empty heart-rate field is a dropped sample and is returned as 0.0.
    Returns a list of floats in bpm, in the order they appear in the file.
    """
    readings_bpm = []
    header_seen = False
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            if not header_seen:
                header_seen = True
                continue
            time_text, hr_text = line.split(",")
            if hr_text == "":
                readings_bpm.append(0.0)
            else:
                readings_bpm.append(float(hr_text))
    return readings_bpm


# PROMPT (final version used, week 3):
# Write a Python function percent_above(readings, limit_bpm).
# readings is a list of heart rates in bpm; a reading of 0 means a dropped
# sample and anything above 250 bpm is an artefact — neither is part of the
# recording. limit_bpm is the limit in bpm; a reading exactly equal to it
# does not count as above. Return the percentage of the remaining readings
# that are above the limit, rounded to one decimal. If there are no valid
# readings, raise a ValueError. Type hints and a docstring stating the units.
# Plain Python, no packages.
def percent_above(readings: list[float], limit_bpm: float) -> float:
    """Percentage (0-100, one decimal) of the valid readings above limit_bpm.

    Readings of 0 (dropped samples) and above 250 bpm (artefacts) are ignored.
    A reading exactly equal to limit_bpm does not count as above.
    Raises ValueError if there are no valid readings.
    """
    valid = 0
    above = 0
    for hr in readings:
        if hr != 0 and hr <= 250:
            valid = valid + 1
            if hr > limit_bpm:
                above = above + 1
    if valid == 0:
        raise ValueError("no valid readings")
    return round(100 * above / valid, 1)


# PROMPT (final version used):
# Write a Python function make_recording_file(path, n_total, n_above, limit_bpm)
# that writes a heart-rate file in exactly the same format as the wearable:
# one line '# made by make_recording_file', then the header 'time_s,hr_bpm',
# then n_total lines 'time,heart rate', with times 0, 15, 30, ... seconds.
# The first n_above heart rates are limit_bpm + 10; the others are
# limit_bpm - 10. Write whole numbers. No dropped samples, no artefacts.
# Raise ValueError if n_above > n_total. Open with encoding="utf-8".
# Type hints and a docstring. Plain Python, no packages.
def make_recording_file(path, n_total: int, n_above: int, limit_bpm: float) -> None:
    """Write a wearable-format file of n_total readings, n_above above limit_bpm.

    Readings above the limit are limit_bpm + 10 bpm, the rest limit_bpm - 10 bpm,
    one every 15 s. The answer of percent_above on it is known by construction:
    100 * n_above / n_total.
    """
    if n_above > n_total:
        raise ValueError("n_above cannot be larger than n_total")
    with open(path, "w", encoding="utf-8") as file:
        file.write("# made by make_recording_file\n")
        file.write("time_s,hr_bpm\n")
        for i in range(n_total):
            if i < n_above:
                hr_bpm = limit_bpm + 10
            else:
                hr_bpm = limit_bpm - 10
            file.write(f"{i * 15},{hr_bpm:.0f}\n")


# =====================================================================
# ASSIGNMENT 4 — your two steps. The names and inputs are fixed:
# do not rename them, and do not change the parameters.
# Replace each placeholder PROMPT with the final prompt you sent, and each
# "raise NotImplementedError" with the body that came back.
# =====================================================================


# PROMPT (final version used):
# fill in `fill_gaps` in vitals.py, keeping the signature unchanged
#
# The readings_bpm list will be from `data/night.csv` so some bpm values will be empty.
# The empty values or values that are <=0 or >250 will be treated as artifacts and will be
# normalised by linear interpolation between the nearest neighbours
# (and if none then the neighbour will be treated as 0).
# The input list should not be modified. A fresh one should be generated for the return value.
#
# Fill in the docstring below the signature and leave the comment above unchanged
def fill_gaps(readings_bpm: list[float]) -> list[float]:
    """Fill gaps (artifacts) in a heart-rate list by linear interpolation.

    Units: beats per minute (bpm).

    Invalid readings (artifacts) are those <= 0 or > 250. These values are
    replaced by values linearly interpolated between the nearest valid
    neighbours. If a neighbour is missing (gap at the start or end, or there
    are no valid readings at all) that neighbour is treated as 0.0 for the
    purposes of interpolation. The input list is not modified; a new list of
    floats is returned.
    """
    if readings_bpm is None:
        return []

    n = len(readings_bpm)
    if n == 0:
        return []

    # Work from a float copy so the input is not mutated.
    orig = [float(x) for x in readings_bpm]
    result = orig.copy()

    def is_valid(v: float) -> bool:
        return v > 0 and v <= 250

    i = 0
    while i < n:
        if is_valid(orig[i]):
            i += 1
            continue

        # Start of a run of invalid values
        start = i
        while i < n and not is_valid(orig[i]):
            i += 1
        end = i - 1

        # Find nearest valid to the left
        left_idx = start - 1
        while left_idx >= 0 and not is_valid(orig[left_idx]):
            left_idx -= 1
        left_val = orig[left_idx] if left_idx >= 0 else 0.0

        # Find nearest valid to the right
        right_idx = i
        while right_idx < n and not is_valid(orig[right_idx]):
            right_idx += 1
        right_val = orig[right_idx] if right_idx < n and is_valid(orig[right_idx]) else 0.0

        run_len = end - start + 1
        for k in range(1, run_len + 1):
            frac = k / (run_len + 1)
            result[start + k - 1] = left_val + (right_val - left_val) * frac

    return result


# PROMPT (final version used):
# (your prompt for save_recording goes here)
def save_recording(path, readings_bpm: list[float], interval_s: float) -> None:
    raise NotImplementedError("save_recording: body not written yet")
