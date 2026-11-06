# G24/P19 Week 9 design decision — M2 case 15

## Evidence and scope

Our frozen M2 case 15 is [`alldatacenter/alldata` commit `d361345e`](https://github.com/alldatacenter/alldata/commit/d361345e59dca612383385b4a4d255c28034b7eb), compared with first parent `0336a1ae`. The published and reproduced maximum-depth increase is **13**: depth **1 → 14**, above the Java threshold of **12**. This M2 result remains unchanged.

The two deepest tracked paths are inside `data-spider/spider/venv/Lib/site-packages/pip-9.0.1-py3.6.egg/pip/_vendor/...`. Of 683 tracked paths after the commit, 307 are under `data-spider/spider/venv/`. [`case15-triage.json`](case15-triage.json) records a separate diagnostic: if exactly that virtual-environment prefix is omitted, the maximum depth is **1 → 8**, an increase of **7**, below the original threshold. This identifies the virtual environment as necessary for this case to cross the threshold; it does not change the paper's metric or prove a source-code design flaw.

## Design pressure and options

The depth alert alone cannot tell a maintainer whether the deepest path is application source or bundled environment content. That is a problem in **interpreting the analysis output**. It also raises a repository-management question about committing an entire virtual environment, but the saved path lists alone cannot establish whether removing it would preserve the original project's build or runtime behaviour.

1. **Leave the analysis output unchanged and explain this case manually.** Lowest implementation cost, but every future reader must rediscover the path origin.
2. **Remove virtual-environment paths from the main metric.** This would suppress the outlier in case 15, but would change the frozen paper method and might hide other relevant changes. We reject this as the main M2 measure.
3. **Remove the tracked virtual environment from the original repository and add an ignore rule.** This could clean that repository, but requires a reliable environment reconstruction route and build/runtime checks. We have not established those checks for this historical third-party project, so we do not claim this cleanup is safe or completed.
4. **Keep the original metric and add a separate path-origin diagnostic.** This preserves comparability with M2 and gives a maintainer the concrete paths behind the alert. We chose this bounded intervention for our analysis tooling.

## Chosen work and verification

[`analyze_case15.py`](analyze_case15.py) reads the saved first-parent and commit path lists from M2, checks the frozen case IDs and 1 → 14 result, then writes [`case15-triage.json`](case15-triage.json). It does not rewrite any M2 evidence or change the threshold. Re-running it refuses to overwrite a differing diagnostic.

An independent `git ls-tree -r -z --name-only` check on the local historical Git objects gave: parent **2 files, depth 1**; commit **683 files, depth 14**; after excluding `data-spider/spider/venv/` only for the diagnostic, **376 files, depth 8**. The frozen M2 result remains **13 ≥ 12**. The diagnostic result is **7 < 12**.

This verifies path counts and depth arithmetic only. We did not change the historical repository, run its application, or verify that deleting a committed environment would preserve behaviour. One selected outlier is not enough to estimate how often this issue occurs across repositories.
