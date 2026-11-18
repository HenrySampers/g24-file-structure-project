G24 / P19 - Week 6 RQ1 reproduction evidence

Scope
-----
The fixed sample is in rq1-cases.txt: 15 commits in 14 Java repositories.
The source is Zenodo record 20601252, version 1, file
Thesis-FileStructureAnalysis-main/labs/max_depth_diff_99_pc.csv.

Current state
-------------
All 15 cases have completed depth measurements matching the authors'
released increases and outlier decisions. The RQ1 reproduction is
REPRODUCED under the group's decision rule. Two group members labelled
the cause of every case on their own, and the labels were then compared
with the authors' cause labels (see rq1-cause-comparison.csv and
tracker I28).

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
rq1-labels-member-1.csv: member 1's cause labels for all 15 cases.
rq1-labels-member-2.csv: member 2's cause labels for all 15 cases.
rq1-cause-comparison.csv: both labels, the agreed label, the authors'
label, whether they match, and notes on each disagreement.

Procedure
---------
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
6. Preserve raw evidence and any failures. The result is in tracker I28
   and the link to this evidence location is in J28.
