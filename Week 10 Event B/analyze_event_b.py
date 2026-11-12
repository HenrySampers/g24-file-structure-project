"""Reproduce the bounded P19 Event B path-placement comparison.

This models path placement only. It does not write to the historical repository
or claim that the proposed feature compiles or works.
"""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CASE = ROOT / "Week 06 Project Work" / "case-15"
COMMIT = "d361345e59dca612383385b4a4d255c28034b7eb"
PARENT = "0336a1ae49f8d2102e57454abdbd76c9da685e09"
VENV_PREFIX = "data-spider/spider/venv/"
PROPOSED = (
    "data-spider/spider/ArticleSpider/spiders/newssite.py",
    "data-spider/spider/ArticleSpider/models/news_article.py",
    "data-spider/spider/ArticleSpider/utils/news_parser.py",
    "data-spider/spider/ArticleSpider/resources/news_selectors.json",
)


def saved_tree_paths(filename: str) -> set[str]:
    # These null-delimited git ls-tree outputs are committed with the M2 case.
    raw = (CASE / filename).read_bytes()
    if not raw.endswith(b"\0"):
        raise ValueError(f"Incomplete saved tree list: {filename}")
    paths = [part.decode("utf-8", errors="surrogateescape") for part in raw.split(b"\0") if part]
    if len(paths) != len(set(paths)):
        raise ValueError(f"Duplicate paths in saved tree list: {filename}")
    return set(paths)


def depth(path: str) -> int:
    return path.count("/") + 1


def measure(paths: set[str]) -> dict[str, int]:
    return {"tracked_path_count": len(paths), "maximum_file_depth": max(map(depth, paths), default=0)}


def directories(paths: set[str]) -> set[str]:
    result = set()
    for path in paths:
        parts = path.split("/")
        result.update("/".join(parts[:index]) for index in range(1, len(parts)))
    return result


def main() -> None:
    if len(PROPOSED) != 4 or len(set(PROPOSED)) != 4:
        raise ValueError("The fixed four-path scope was changed")
    measurement = json.loads((CASE / "measurement.json").read_text(encoding="utf-8"))
    if measurement["commit"] != COMMIT or measurement["first_parent"] != PARENT:
        raise ValueError("Saved M2 case IDs do not match the frozen Event B case")
    parent = saved_tree_paths("before-paths.raw")
    baseline = saved_tree_paths("after-paths.raw")
    if measure(parent)["maximum_file_depth"] != 1 or measure(baseline)["maximum_file_depth"] != 14:
        raise ValueError("Saved M2 path depths differ from the frozen case-15 result")
    overlap = baseline.intersection(PROPOSED)
    if overlap:
        raise ValueError(f"Proposed paths already exist: {sorted(overlap)}")
    future = baseline.union(PROPOSED)
    new_directories = sorted(directories(future) - directories(baseline))
    co_located_paths = set(PROPOSED)
    co_located_paths.remove("data-spider/spider/ArticleSpider/resources/news_selectors.json")
    co_located_paths.add("data-spider/spider/ArticleSpider/utils/news_selectors.json")
    co_located_future = baseline.union(co_located_paths)
    without_venv = lambda paths: {p for p in paths if not p.startswith(VENV_PREFIX)}

    # M4 added an analysis-only path-origin check. It did not edit the
    # application tree, so pre-M4 and M4 path placements are intentionally equal.
    layouts = {}
    for name in ("pre_m4_application_structure", "m4_application_structure"):
        layouts[name] = {
            "proposed_paths": list(PROPOSED),
            "required_new_files": len(future - baseline),
            "new_directories": new_directories,
            "existing_files_moved": len(baseline - future),
            "existing_files_deleted": len(baseline - future),
            "extra_file_changes_beyond_fixed_feature_paths": 0,
            "after_feature": measure(future),
            "new_feature_depth_increase": measure(future)["maximum_file_depth"] - measure(baseline)["maximum_file_depth"],
        }

    result = {
        "scope": "Reasoned path-placement comparison; no application files were created, moved, compiled or tested",
        "source_commit": COMMIT,
        "source_first_parent": PARENT,
        "source_path_lists": ["Week 06 Project Work/case-15/before-paths.raw", "Week 06 Project Work/case-15/after-paths.raw"],
        "frozen_week9_tag": "PRE_EVENT_B",
        "threshold": 12,
        "first_parent": measure(parent),
        "source_commit_tree": measure(baseline),
        "source_commit_without_venv_diagnostic": measure(without_venv(baseline)),
        "tracked_venv_paths": len(baseline) - len(without_venv(baseline)),
        "proposed_feature_path_depths": {p: depth(p) for p in PROPOSED},
        "layouts": layouts,
        "comparison": {
            "difference_in_required_new_files": 0,
            "difference_in_new_directories": 0,
            "difference_in_existing_files_moved_or_deleted": 0,
            "avoidable_structural_file_churn_shown_by_m4": 0,
            "explanation": "M4 changed only analysis output, so it cannot place the application feature differently without a further design change.",
        },
        "alternative_co_locate_resource_in_existing_utils": {
            "proposed_paths": sorted(co_located_paths),
            "after_feature": measure(co_located_future),
            "new_directories": sorted(directories(co_located_future) - directories(baseline)),
            "existing_files_moved_or_deleted": 0,
        },
        "frozen_case15_outlier_increase": measure(baseline)["maximum_file_depth"] - measure(parent)["maximum_file_depth"],
        "feature_extension_outlier_increase": measure(future)["maximum_file_depth"] - measure(baseline)["maximum_file_depth"],
        "m4_diagnostic_max_depth_after_feature": measure(without_venv(future))["maximum_file_depth"],
    }
    output = HERE / "path-comparison.json"
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    print(json.dumps(result["comparison"], indent=2))


if __name__ == "__main__":
    main()
