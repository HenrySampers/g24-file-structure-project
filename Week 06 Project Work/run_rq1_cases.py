"""Collect RQ1 Git evidence for the fixed cases without changing the sample."""

import csv
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ROWS = list(csv.DictReader((ROOT / "rq1-results.csv").open(newline="", encoding="utf-8")))
REPOS = ROOT / "repos"
ENV = os.environ.copy()
ENV["GIT_TERMINAL_PROMPT"] = "0"


def run(args, timeout=300):
    result = subprocess.run(
        args, cwd=ROOT, env=ENV, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=timeout, check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"{' '.join(args)} failed ({result.returncode}): {detail}")
    return result.stdout


def git_args(repo, *args):
    return ["git", "-c", f"safe.directory={repo}", "-C", str(repo), *args]


def git(repo, *args):
    return run(git_args(repo, *args))


def has_commit(repo, oid):
    return subprocess.run(
        git_args(repo, "cat-file", "-e", f"{oid}^{{commit}}"), cwd=ROOT, env=ENV,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def save_once(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"Existing evidence differs; not overwriting {path}")
        return
    path.write_bytes(data)


def save_lines_once(path, data):
    if path.exists():
        if path.read_bytes().splitlines() != data.splitlines():
            raise RuntimeError(f"Existing evidence differs; not overwriting {path}")
        return
    path.write_bytes(data)


def record_case(row):
    number = row["case"]
    case_dir = ROOT / f"case-{number}"
    case_dir.mkdir(exist_ok=True)
    repo = REPOS / row["repository"].replace("/", "__")
    repo_url = f"https://github.com/{row['repository']}.git"
    commit = row["commit_id"]
    parent = row["parent_id"]
    prefix = "case-01-" if number == "01" else ""

    if not repo.exists():
        run(["git", "init", str(repo)])
        git(repo, "remote", "add", "origin", repo_url)

    # Existing histories can be rechecked offline; fetch only missing commits.
    if not has_commit(repo, commit) or not has_commit(repo, parent):
        git(repo, "-c", "http.sslBackend=openssl", "fetch", "--no-tags",
            "--filter=blob:none", "--depth=2", "origin", commit)
    actual_parent = git(repo, "rev-parse", f"{commit}^1").decode().strip()
    if actual_parent != parent:
        raise RuntimeError(f"CSV first parent {parent} != Git first parent {actual_parent}")

    trees = {}
    paths = {}
    for label, oid in (("before", parent), ("after", commit)):
        raw = git(repo, "ls-tree", "-r", "-z", "--name-only", oid)
        save_once(case_dir / f"{label}-paths.raw", raw)
        names = [p for p in raw.split(b"\0") if p]
        save_lines_once(case_dir / f"{prefix}{label}-paths.txt",
                        b"\n".join(names) + (b"\n" if names else b""))
        trees[label] = len(names)
        paths[label] = max((p.count(b"/") + 1 for p in names), default=0)

    message = git(repo, "show", "-s", "--format=fuller", commit)
    changed = git(repo, "diff", "--name-status", "--no-renames", parent, commit)
    if number == "01":
        save_once(case_dir / "commit-message.raw", message)
        old_message = case_dir / "case-01-commit-message.txt"
        if old_message.exists():
            if commit.encode() not in old_message.read_bytes():
                raise RuntimeError(f"Existing commit message does not identify {commit}")
        else:
            old_message.write_bytes(message)
    else:
        save_once(case_dir / "commit-message.txt", message)
    save_lines_once(case_dir / f"{prefix}changed-paths.txt", changed)
    deepest = [p for p in git(repo, "ls-tree", "-r", "-z", "--name-only", commit).split(b"\0")
               if p and p.count(b"/") + 1 == paths["after"]]
    save_lines_once(case_dir / f"{prefix}deepest-paths.txt",
                    b"\n".join(deepest) + b"\n")

    increase = paths["after"] - paths["before"]
    threshold = float(row["java_threshold"])
    authors_increase = float(row["authors_increase"])
    authors_after = int(row["authors_max_depth"])
    result = {
        "case": number,
        "repository": row["repository"],
        "repo_url": repo_url,
        "commit": commit,
        "first_parent": parent,
        "source_csv": "Zenodo 20601252 v1 / labs/max_depth_diff_99_pc.csv",
        "git_route": {
            "fetch": "git fetch --no-tags --filter=blob:none --depth=2 origin <commit>",
            "tree": "git ls-tree -r -z --name-only <commit-or-first-parent>",
            "diff": "git diff --name-status --no-renames <first-parent> <commit>",
        },
        "file_count_before": trees["before"],
        "file_count_after": trees["after"],
        "max_depth_before": paths["before"],
        "max_depth_after": paths["after"],
        "increase": increase,
        "authors_max_depth_after": authors_after,
        "authors_increase": authors_increase,
        "java_threshold": threshold,
        "our_outlier_decision": increase >= threshold,
        "authors_outlier_decision": authors_increase >= threshold,
        "numeric_match": increase == authors_increase and
                         (increase >= threshold) == (authors_increase >= threshold),
        "cause_label_status": "awaiting_two_independent_group_member_labels",
        "raw_evidence_directory": case_dir.name,
    }
    save_once(case_dir / "measurement.json", (json.dumps(result, indent=2) + "\n").encode())
    return result


def main():
    REPOS.mkdir(exist_ok=True)
    selected = set(sys.argv[1:] or [row["case"] for row in ROWS])
    failures = 0
    for row in ROWS:
        if row["case"] not in selected:
            continue
        number = row["case"]
        print(f"Case {number}: {row['repository']} {row['commit_id']}", flush=True)
        try:
            result = record_case(row)
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
            path = ROOT / f"case-{number}" / "failure.txt"
            save_once(path, (str(exc) + "\n").encode("utf-8", "replace"))
            print(f"  BLOCKED: {exc}", flush=True)
            failures += 1
            continue
        print(f"  {result['max_depth_before']} -> {result['max_depth_after']} "
              f"= {result['increase']}; match={result['numeric_match']}", flush=True)
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
