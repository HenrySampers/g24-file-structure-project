# G24 / P19 — Outliers in File-Structure Evolution

CS4928 Theory and Practice of Software Design, 2026/27 group project.

- **Study:** Logemann et al., *On the outliers of file-structure evolution: a mining study of GitHub software repositories*, Empirical Software Engineering (2026). https://link.springer.com/article/10.1007/s10664-026-10891-7
- **Artefact:** Zenodo record 20601252, version 1 (`Thesis-FileStructureAnalysis-main.zip`). https://zenodo.org/records/20601252
- **Group:** Henry Sampers, David Bradshaw, Fuwhad Akinwale, Rayan Blaq, Donal Reynolds

## What is in this repository

| Folder | Stage | Main files |
| --- | --- | --- |
| `Week 05 M1 Plan/` | M1: plan | `G24_P19_Week05_M1.md` |
| `Week 06 Project Work/` | M2: bounded reproduction (RQ1) | `rq1-cases.txt` (fixed 15 cases and selection rule), `rq1-results.csv` (our depths vs the authors'), `rq1-labels-member-1.csv`, `rq1-labels-member-2.csv`, `rq1-cause-comparison.csv`, `case-01` … `case-15` (raw Git path lists and measurements) |
| `Week 07 Event A/` | Change Event A | `README.md`, `frozen-results.csv`, `case-01` … `case-20` |
| `Week 09 Design Decision/` | M4: design decision | `README.md`, `analyze_case15.py`, `case15-triage.json` |
| `Week 10 Event B/` | Change Event B | `prediction.md` (recorded before the comparison), `README.md`, `analyze_event_b.py`, `path-comparison.json` |

Each stage folder has its own README explaining the method, the result and the limits. How we used AI, and how we checked it, is in [`AI_USE.md`](AI_USE.md).

## Tags

| Tag | Commit | State |
| --- | --- | --- |
| `M2_REPRO` | `5b57d2f` | Bounded reproduction complete (added retroactively; see the tag message) |
| `PRE_EVENT_A` | `5b57d2f` | Frozen state before Event A (added retroactively; see the tag message) |
| `PRE_EVENT_B` | `ffe5a11` | Week 9 design decision, frozen before Event B |

## Metric

For a commit and its first parent, list every tracked file with `git ls-tree -r -z --name-only`. A file's depth is its number of path components (a root file has depth 1). Take the maximum depth in each tree. The increase is the commit's maximum minus the parent's maximum. A Java commit is an outlier when the increase is at least **12**, the released Java threshold in `labs/max_depth_diff_99_pc.csv`.

## Requirements

- Python 3 (we used 3.14.6), standard library only
- Git (we used 2.53.0.windows.1) and internet access to GitHub for the fetch steps

## How to re-run

Run everything from this folder (the repository root). The historical repositories are **not** committed. They are downloaded into `Week 06 Project Work/repos/`, which is gitignored. Only commit trees are fetched (`--filter=blob:none`), so the downloads are small.

1. **RQ1 evidence.** Fetches each case's commit and first parent and saves the path lists and measurements:

   ```bash
   python "Week 06 Project Work/run_rq1_cases.py"
   ```

2. **RQ1 check.** Compares our depths with the authors' CSV and writes `verification.txt`:

   ```bash
   python "Week 06 Project Work/verify_rq1.py"
   ```

3. **Event A.** First fetch the held-out repository (commands in `Week 07 Event A/README.md`), then:

   ```bash
   python "Week 07 Event A/run_event_a.py"
   ```

4. **Week 9 diagnostic.** Works offline from the saved case-15 path lists:

   ```bash
   python "Week 09 Design Decision/analyze_case15.py"
   ```

5. **Event B comparison.** Works offline from the saved case-15 path lists:

   ```bash
   python "Week 10 Event B/analyze_event_b.py"
   ```

The scripts recalculate the results from the Git history and compare them with the saved evidence. They won't overwrite a saved file that differs, so the committed evidence isn't replaced by a re-run.
