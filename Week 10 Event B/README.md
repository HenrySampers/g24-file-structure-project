# G24 / P19 Event B

## What we had to do

Event B asked us to add a new feature that needs several new classes or files, place it in both our structure before Week 9 (pre-M4) and after Week 9 (M4), and see how much extra structural change it causes. We did this as a planned comparison of file paths. We did not build the feature or change the original repository.

Our starting point is tag `PRE_EVENT_B` (commit `ffe5a11`). We wrote our prediction in [`prediction.md`](prediction.md) before running the comparison.

## The feature

We used our M2 case 15 repository, `alldatacenter/alldata` at commit `d361345e`. The feature is a spider for one new news website, which needs 4 new files:

| New file | What it is |
| --- | --- |
| `data-spider/spider/ArticleSpider/spiders/newssite.py` | Spider class |
| `data-spider/spider/ArticleSpider/models/news_article.py` | Article model class |
| `data-spider/spider/ArticleSpider/utils/news_parser.py` | Parser class |
| `data-spider/spider/ArticleSpider/resources/news_selectors.json` | Selectors file |

The `spiders/`, `models/` and `utils/` folders already exist. `resources/` would be a new folder.

The files go in the same place in both structures, because our Week 9 change was a separate check in our analysis and didn't change the repository's folders.

## Result

| | Pre-M4 | M4 |
| --- | ---: | ---: |
| New files | 4 | 4 |
| New folders | 1 | 1 |
| Files moved or deleted | 0 | 0 |
| Tracked files after the feature | 687 | 687 |
| Max file depth after the feature | 14 | 14 |
| Depth increase | 0 | 0 |

The repository already has 683 files with a max depth of 14, which comes from the committed `venv/` folder. The new files are only depth 5, so the max depth stays at 14 and the increase is 0. That is under the Java threshold of 12, so there is no new outlier. Our Week 9 check, which leaves out `venv/`, stays at depth 8.

So the M4 structure saves **0** structural changes compared to pre-M4.

## Options we considered

1. **Keep our Week 9 check and add the feature in the existing folders.** This is the smallest change, so we chose it.
2. **Put the selectors file in `utils/` so we don't need a new folder.** We didn't do this because it mixes config with code, and we had no evidence it helps.
3. **Remove the committed `venv/` from the repository.** That is 307 files and would need build and dependency checks we haven't done, so we didn't do it.

## Decision

Our Week 9 decision is **partly supported**. The check still explains why case 15 was an outlier, but it doesn't reduce any structural change when adding a new feature.

The trade-off we accepted is keeping the extra `resources/` folder and the committed `venv/`, so our results stay comparable with M2. The risk that is still there is that treating every depth alert as a design problem could lead to refactoring that isn't needed.

## How to run it

From the repository root:

```bash
python "Week 10 Event B/analyze_event_b.py"
```

It reads the saved case 15 files in `Week 06 Project Work/case-15/` and writes [`path-comparison.json`](path-comparison.json). It doesn't need the original repository downloaded.

## Limits

This is a planned file-path comparison, not real code. We checked the file counts and depths against the Git trees, but we did not build, test or run the feature, so we can't say it would work or that the result applies to other features.
