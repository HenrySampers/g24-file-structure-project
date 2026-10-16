G24 / P19 - Week 6 RQ1 reproduction evidence

Scope
-----
The fixed sample is in rq1-cases.txt: 15 commits in 14 Java repositories.
The source is Zenodo record 20601252, version 1, file
Thesis-FileStructureAnalysis-main/labs/max_depth_diff_99_pc.csv.

Current state
-------------
All 15 cases have completed depth measurements matching the authors'
released increases and outlier decisions. The RQ1 reproduction is still
IN PROGRESS, not yet REPRODUCED under the group's full decision rule:
two independent group-member cause labels and comparison with the
authors' cause labels remain. No human or author cause labels have been
entered in these files.

Files
-----
rq1-cases.txt: fixed case list and selection rule (already present).
rq1-results.csv: current 15-case numerical results table.
case-01 directory: original PowerShell evidence and the collector's raw
Git paths, commit message and measurement.json. The original text files
are retained and checked, not overwritten.
case-02 through case-15 directories: raw Git paths, commit message,
changed paths, deepest paths and measurement.json for each case.
repos directory: 14 normal Git repositories (one per source repository),
named owner__repository. These contain Git history for the sampled
commits. Most have no checked-out project files; an interrupted checkout
left aberic__fabric-net-server partially populated, so do not treat its
working tree as complete. These are local inputs, not part of the
evidence to upload to the group's GitHub repository.
run_rq1_cases.py: repeatable evidence collection for all 15 cases.
verify_rq1.py and verification.txt: automated check of fixed selection,
source values, saved raw paths and reported depth results (PASS).
rq1-context-summary.txt: objective path/change context for cause review.
rq1-labels-member-1.txt and rq1-labels-member-2.txt: separate blank
cause-review forms for the whole sample.
rq1-cause-comparison.csv: blank table for agreed labels and comparison
with the authors after both independent reviews are saved.

Procedure and pending work
--------------------------
1. Keep the fixed case even if its history cannot be accessed. Record the
   issue; do not substitute a more convenient commit.
2. Obtain the exact commit and first parent listed in rq1-results.csv.
   Save the tracked file paths from both Git trees and the command route.
3. Count path components (a root file has depth 1), take each tree's
   maximum, and subtract before from after. Compare the increase and
   >= 12 decision with the released CSV values.
4. Save the changed-path list and commit message. Two group members
   independently record a cause and supporting paths/context before
   seeing each other's label or the authors' classification.
5. After both labels are saved, resolve any disagreement, then compare
   with the authors' label. Keep all original labels and disagreements.
6. Preserve raw evidence and any failures. Report a current status in
   tracker I28 and a link to this evidence location in J28. Do not claim
   the whole sample is reproduced from the pilot alone.

These files do not show that the group completed a coordinator checkpoint
or the required independent human cause review.
