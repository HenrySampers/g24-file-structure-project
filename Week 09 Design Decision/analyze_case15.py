"""Audit the path source of M2 case 15 without changing its frozen result.

Run from the project root: python "Week 09 Design Decision/analyze_case15.py"
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CASE = ROOT / "Week 06 Project Work" / "case-15"
OUTPUT = Path(__file__).resolve().parent / "case15-triage.json"
VENV_PREFIX = b"data-spider/spider/venv/"
COMMIT = "d361345e59dca612383385b4a4d255c28034b7eb"
PARENT = "0336a1ae49f8d2102e57454abdbd76c9da685e09"
THRESHOLD = 12


def paths(filename):
    return [item for item in (CASE / filename).read_bytes().split(b"\0") if item]


def maximum_depth(items):
    return max((item.count(b"/") + 1 for item in items), default=0)


def main():
    measurement = json.loads((CASE / "measurement.json").read_text(encoding="utf-8"))
    assert (measurement["commit"], measurement["first_parent"]) == (COMMIT, PARENT)
    before = paths("before-paths.raw")
    after = paths("after-paths.raw")
    before_depth = maximum_depth(before)
    after_depth = maximum_depth(after)
    assert (before_depth, after_depth, after_depth - before_depth) == (1, 14, 13)

    # This is a diagnostic of one path origin, not a replacement for the M2 method.
    before_other = [item for item in before if not item.startswith(VENV_PREFIX)]
    after_other = [item for item in after if not item.startswith(VENV_PREFIX)]
    after_venv = [item for item in after if item.startswith(VENV_PREFIX)]
    without_depth = maximum_depth(after_other)
    result = {
        "repository": "alldatacenter/alldata",
        "commit": COMMIT,
        "first_parent": PARENT,
        "threshold": THRESHOLD,
        "frozen_m2": {
            "before_max_depth": before_depth,
            "after_max_depth": after_depth,
            "increase": after_depth - before_depth,
            "outlier": after_depth - before_depth >= THRESHOLD,
        },
        "diagnostic_excluding_exact_venv_prefix": {
            "excluded_prefix": VENV_PREFIX.decode(),
            "tracked_venv_paths_at_commit": len(after_venv),
            "tracked_other_paths_at_commit": len(after_other),
            "before_max_depth": maximum_depth(before_other),
            "after_max_depth": without_depth,
            "increase": without_depth - maximum_depth(before_other),
            "would_meet_original_threshold": without_depth - maximum_depth(before_other) >= THRESHOLD,
        },
        "deepest_paths": [
            item.decode("utf-8", "replace") for item in after
            if item.count(b"/") + 1 == after_depth
        ],
        "interpretation": "Path-origin diagnostic only; original M2 outlier result remains 13 >= 12.",
    }
    data = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if OUTPUT.exists() and OUTPUT.read_bytes() != data:
        raise RuntimeError(f"Existing diagnostic differs: {OUTPUT}")
    if not OUTPUT.exists():
        OUTPUT.write_bytes(data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
