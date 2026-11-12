# G24/P19 Event B prediction and fixed scope

This file records the prediction **before** the Event B path comparison. The frozen Week 9 state is repository tag `PRE_EVENT_B` (`ffe5a116d372802c4745639d24aeaa5de69f6a22`). The historical application case is `alldatacenter/alldata` commit `d361345e59dca612383385b4a4d255c28034b7eb`.

## Bounded new feature

Consider adding a spider for one new news website to the existing `data-spider/spider/ArticleSpider` project. For a reasoned structural comparison, the proposed feature requires these four new tracked paths:

1. `data-spider/spider/ArticleSpider/spiders/newssite.py` — spider class.
2. `data-spider/spider/ArticleSpider/models/news_article.py` — article model class.
3. `data-spider/spider/ArticleSpider/utils/news_parser.py` — page parser class.
4. `data-spider/spider/ArticleSpider/resources/news_selectors.json` — selector resource.

This is a **path-level design scenario**, not a claim that these classes were implemented, integrated, tested or added by the original developers. The four paths and the historical commit are fixed before measurement. A real feature would need implementation, integration and behaviour tests; those are outside this bounded comparison.

## Prediction before comparison

The proposed feature belongs under the existing `ArticleSpider` source tree. The Week 9 intervention changed our **analysis output** by adding a separate path-origin diagnostic; it did not change the historical application's folders. We therefore predict that the four new paths will be placed identically in the pre-M4 and M4 structures, with no difference in file additions or moves. The already committed virtual environment is likely to remain the deepest part of the repository, so the original maximum-depth measure may not flag this feature at all. If so, the path check will not reduce structural churn from adding the feature. It remains useful only when an outlier needs interpretation.

An outcome that would challenge this prediction would be a defensible different placement in the M4 structure, fewer necessary path changes there, or a new depth alert whose interpretation materially changes because of the diagnostic.
