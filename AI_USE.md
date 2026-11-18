# G24 / P19 — AI use

We used AI as an assistant during the project. The brief says AI output is not evidence by itself, so below is where AI was used and how we checked it.

## Writing the scripts

We used AI to write the Python scripts (`run_rq1_cases.py`, `verify_rq1.py`, `run_event_a.py`, `analyze_case15.py`, `analyze_event_b.py`).

How we checked it:
- The RQ1 depth results from the scripts match the authors' released values in 15/15 cases (`Week 06 Project Work/verification.txt`).
- For Week 9 we checked the case 15 counts and depths with our own `git ls-tree` commands against the Git history, and they matched the script (see `Week 09 Design Decision/README.md`).
- The scripts save their raw Git output and refuse to overwrite saved evidence that differs, so re-running them confirms the results.

## Understanding the events and what we had to do

We used AI to help us understand the Event A and Event B sheets and what each stage of the project asked for. We checked this against the event sheets and the project brief themselves. The decisions in Event A, Week 9 and Event B were made by the group.

## Finding points in the original paper

We used AI to help find the relevant sections of the paper, such as the outlier sampling, the file depth metric, the Java threshold of 12 and the outlier cause categories. We then read those sections in the paper ourselves. The threshold and the authors' cause labels we compare against come from the authors' released data (Zenodo record 20601252), not from AI.
