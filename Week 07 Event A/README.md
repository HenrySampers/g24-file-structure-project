# P19 Event A — held-out file-depth check

## Fixed material and method

- Repository: [`macrozheng/mall`](https://github.com/macrozheng/mall), a Java repository present in the study artefact's `datasets/github_data_07_03_2024.csv` and absent from our 15 M2 cases.
- Window: 20 consecutive first-parent commits, oldest [`83abb8e`](https://github.com/macrozheng/mall/commit/83abb8e12940519121e74d372e47a4df30e216dc) through newest [`dcaa93b`](https://github.com/macrozheng/mall/commit/dcaa93b3150352e5044708d7211b5bed0af4509f), with [`dd6569c`](https://github.com/macrozheng/mall/commit/dd6569c3558f79af5b21aad601349e0f029b9a6d) as the oldest commit's baseline parent. The script verifies this entire chain before measuring.
- Selection was fixed from repository and commit metadata before file paths, depth measurements, and causes were examined. The Event A prediction was entered in the shared Student Tracker before execution; the tracker is the record of that prediction.
- Frozen M2 metric: for each commit and its first parent, list all tracked file paths with `git ls-tree -r -z --name-only`; file depth is the number of path components; take the maximum in each tree; increase is after minus before. A Java outlier has increase **at least 12**. No threshold or sample change was made after looking at the result.

## Frozen first result

[`frozen-results.csv`](frozen-results.csv) contains all 20 commits and calculations. Each `case-XX` folder contains raw before/after path lists, changed paths, deepest paths, the raw Git commit object, and a measurement JSON file. [`run_event_a.py`](run_event_a.py) produced these files and refuses to overwrite differing evidence.

**0/20 outliers.** All 20 measured increases were 0. For cases 01–17, maximum depth was 11 before and after with 719 tracked files. Case 18 had depth 11 before and after, with file count 719 → 717. Cases 19–20 also retained maximum depth 11, with 717 files. The frozen Java threshold of 12 therefore flagged no commits.

## Diagnostic check after the frozen result

Case 18 ([commit `0504e86`](https://github.com/macrozheng/mall/commit/0504e86b1f1b6f1b8aa6a734d37a90fb67346be7)) added five paths and deleted seven. Most other file changes were edits at existing paths, which cannot by themselves change file depth. Five Maven `pom.xml` build/dependency descriptors were edited at their existing paths (`pom.xml`, `mall-admin/pom.xml`, `mall-common/pom.xml`, `mall-mbg/pom.xml`, and `mall-security/pom.xml`). The before and after trees each contain eight `pom.xml` files, at depth 1 or 2. If those eight paths are omitted solely as a diagnostic, the maximum depth is still 11 before and after. This check does **not** alter the frozen result. No added path in this 20-commit window was visibly under common generated/vendor/dependency directories such as `target/`, `build/`, `node_modules/`, or `vendor/`.

The observed Maven changes did not distort this window's maximum-depth signal. Since no threshold crossing occurred, this window cannot establish what proportion of outliers caused by generated or dependency files would be false signals in a broader sample.

## Comparison and design implication

M2 deliberately sampled 15 known Java outliers from the authors' released results; all 15 had depth increases of at least 12, and our calculations matched the authors in 15/15. This held-out, consecutive window yielded 0/20 outliers using the same metric and threshold. The **calculation and threshold transfer** to a new repository/window; the M2 frequency and cause mix do **not** transfer from a sample selected for outliers to this ordinary commit window. We also cannot compare cause labels, because no Event A commit was flagged for outlier classification.

For repository maintenance, a depth alert should prompt inspection of the paths that set the new maximum and the commit context before deciding on refactoring or tooling. In case 18, the added and deleted paths did not change the maximum depth; edits to existing files are irrelevant to that calculation. No structure-driven refactoring is justified by this Event A result alone.

## Reproduction

The fetched repository lives under the ignored `Week 06 Project Work/repos/macrozheng__mall` directory. From the project root, run `python "Event A/run_event_a.py"`. The script checks the fixed 21-commit chain, recalculates every case and confirms that existing evidence agrees byte for byte. The GitHub evidence repository should contain this `Event A` folder; the Git object database itself is intentionally excluded.
