"""Frozen P19 Event A measurement for the preselected 20 mall commits.

Run from any directory with: python "Event A/run_event_a.py"
The repository must already be fetched into Week 06 Project Work/repos/macrozheng__mall.
Existing evidence is never silently replaced.
"""

import csv
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
REPO = PROJECT / "Week 06 Project Work" / "repos" / "macrozheng__mall"
TIP = "dcaa93b3150352e5044708d7211b5bed0af4509f"
OLDEST = "83abb8e12940519121e74d372e47a4df30e216dc"
BASELINE = "dd6569c3558f79af5b21aad601349e0f029b9a6d"
THRESHOLD = 12
ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}


def git(*args):
    result = subprocess.run(
        ["git", "-c", f"safe.directory={REPO}", "-C", str(REPO), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"git {args} failed: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout


def save_once(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"Evidence differs; refusing to overwrite {path}")
    else:
        path.write_bytes(data)


def tracked_paths(oid):
    raw = git("ls-tree", "-r", "-z", "--name-only", oid)
    return raw, [item for item in raw.split(b"\0") if item]


def max_depth(paths):
    return max((path.count(b"/") + 1 for path in paths), default=0)


def main():
    if not REPO.exists():
        raise RuntimeError(f"Fetch the held-out repository first: {REPO}")
    chain = git("rev-list", "--first-parent", "--max-count=21", TIP).decode().splitlines()
    if len(chain) != 21 or chain[19] != OLDEST or chain[20] != BASELINE:
        raise RuntimeError("Fetched first-parent chain does not match the frozen 20-commit selection")

    rows = []
    for n, commit in enumerate(reversed(chain[:20]), 1):
        parent = git("rev-parse", f"{commit}^1").decode().strip()
        expected_parent = BASELINE if n == 1 else rows[-1]["commit_id"]
        if parent != expected_parent:
            raise RuntimeError(f"Unexpected first parent for {commit}: {parent}")
        case_dir = HERE / f"case-{n:02d}"
        case_dir.mkdir(exist_ok=True)
        before_raw, before_paths = tracked_paths(parent)
        after_raw, after_paths = tracked_paths(commit)
        before = max_depth(before_paths)
        after = max_depth(after_paths)
        increase = after - before
        deepest = [path for path in after_paths if path.count(b"/") + 1 == after]
        save_once(case_dir / "before-paths.raw", before_raw)
        save_once(case_dir / "after-paths.raw", after_raw)
        save_once(case_dir / "deepest-paths.txt", b"\n".join(deepest) + (b"\n" if deepest else b""))
        save_once(case_dir / "changed-paths.txt", git("diff", "--name-status", "--no-renames", parent, commit))
        save_once(case_dir / "raw-commit.txt", git("cat-file", "-p", commit))
        row = {
            "case": f"{n:02d}", "commit_id": commit, "first_parent": parent,
            "before_file_count": len(before_paths), "after_file_count": len(after_paths),
            "before_max_depth": before, "after_max_depth": after,
            "depth_increase": increase, "outlier_ge_12": increase >= THRESHOLD,
            "commit_url": f"https://github.com/macrozheng/mall/commit/{commit}",
        }
        save_once(case_dir / "measurement.json", (json.dumps(row, indent=2) + "\n").encode())
        rows.append(row)

    import io
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    save_once(HERE / "frozen-results.csv", output.getvalue().encode("utf-8"))
    print(f"Measured {len(rows)} commits; {sum(row['outlier_ge_12'] for row in rows)} meet the frozen >=12 threshold")
    for row in rows:
        print(row["case"], row["depth_increase"], row["outlier_ge_12"], row["commit_id"])


if __name__ == "__main__":
    main()
