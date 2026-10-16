"""Verify the RQ1 numerical evidence against saved paths and source data."""

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "max_depth_diff_99_pc.csv"
TABLE = ROOT / "rq1-results.csv"
rows = list(csv.DictReader(TABLE.open(newline="", encoding="utf-8")))
source_rows = list(csv.DictReader(SOURCE.open(newline="", encoding="utf-8-sig")))
eligible = [r for r in source_rows if r["lang"] == "Java" and r["parents"].strip()
            and float(r["max_file_depth_diff"]) >= 12]
eligible.sort(key=lambda r: (r["repo_id"], int(r["commit_time"]), r["commit_id"]))

problems = []
report = [
    "G24 / P19 - RQ1 numerical evidence verification",
    "Source: Zenodo 20601252 v1 / labs/max_depth_diff_99_pc.csv",
    "CSV SHA256: " + hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "Git: " + subprocess.check_output(["git", "--version"], text=True).strip(),
    "Python: " + sys.version.split()[0],
    f"Eligible Java source rows: {len(eligible)}",
    f"Fixed sample rows: {len(rows)}",
    "",
    "Case  Before  After  Increase  Author increase  Match",
]

if len(rows) != 15:
    problems.append(f"Expected 15 sample rows, got {len(rows)}")

for index, row in enumerate(rows):
    case = row["case"]
    if index >= len(eligible) or row["commit_id"] != eligible[index]["commit_id"]:
        problems.append(f"Case {case}: not the expected source row in fixed sort order")
        continue
    original = eligible[index]
    if row["parent_id"] != original["parents"]:
        problems.append(f"Case {case}: parent ID differs from source")
    for key, source_key in (("authors_max_depth", "max_file_depth"),
                            ("authors_increase", "max_file_depth_diff"),
                            ("java_threshold", "99%")):
        if float(row[key]) != float(original[source_key]):
            problems.append(f"Case {case}: {key} differs from source")

    folder = ROOT / f"case-{case}"
    prefix = "case-01-" if case == "01" else ""
    measured = {}
    for label in ("before", "after"):
        path = folder / f"{prefix}{label}-paths.txt"
        if not path.exists():
            problems.append(f"Case {case}: missing {path.name}")
            continue
        names = [p for p in path.read_bytes().splitlines() if p]
        measured[label] = max((p.count(b"/") + 1 for p in names), default=0)
        raw = folder / f"{label}-paths.raw"
        if not raw.exists() or [p for p in raw.read_bytes().split(b"\0") if p] != names:
            problems.append(f"Case {case}: readable/raw path lists differ")

    if len(measured) != 2:
        continue
    increase = measured["after"] - measured["before"]
    threshold = float(row["java_threshold"])
    matches = increase == float(row["authors_increase"]) and \
              (increase >= threshold) == (float(row["authors_increase"]) >= threshold)
    if (measured["before"] != int(row["our_before_depth"]) or
            measured["after"] != int(row["our_after_depth"]) or
            increase != int(row["our_increase"]) or
            matches != (row["numeric_match"] == "yes")):
        problems.append(f"Case {case}: results table differs from saved paths")
    result_path = folder / "measurement.json"
    if not result_path.exists():
        problems.append(f"Case {case}: missing measurement.json")
    else:
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if (result["max_depth_before"], result["max_depth_after"], result["increase"]) != \
                (measured["before"], measured["after"], increase):
            problems.append(f"Case {case}: measurement.json differs from saved paths")
    report.append(f"{case:>4}  {measured['before']:>6}  {measured['after']:>5}  "
                  f"{increase:>8}  {float(row['authors_increase']):>15g}  {matches}")

report.extend(["", "Verification: " + ("PASS" if not problems else "FAIL")])
report.extend("- " + problem for problem in problems)
report.append("Cause labels and agreement are not verified here; they remain pending.")
(ROOT / "verification.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
print("\n".join(report))
sys.exit(0 if not problems else 1)
