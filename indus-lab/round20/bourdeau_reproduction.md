# Bourdeau Tamil test: actual reproduction

Checked live repository `dbourdeau/cyphersolver`, commit **843165c369a9c35658b1a7656860e06abd7a5de3**. Executed the original script without parameter changes on 2026-10-11, Python 3.12.14:

```bash
cd /tmp/indus-tamil-audit/targets/indus
python tamil_stars.py
```

Exit 0. Generated report exactly matches the committed report (`git diff --exit-code -- targets/indus/results/tamil_stars.md`, exit 0). This result was independently rerun; other tests below were inspected only.

The script tests whether proposed stroke numerals immediately before fish signs disproportionately take Tamil Lexicon star-name values **3, 5, 6, 7**. It uses bundled `data/corpus.tsv`, `rebus/tlex_star_min.tsv`, `signs.py`, `numerals.py`; standard library only, unsplit signs, seed 53, 10,000 permutations per view.

| Original view | Before fish | Before other signs | One-sided enrichment p |
|---|---:|---:|---:|
| Pairs excluded | 37/86 | 468/746 | 1.0000 |
| Pairs included | 37/297 | 468/1190 | 1.0000 |
| Distinct texts; pairs excluded | 31/71 | 324/572 | 0.9867 |
| Distinct; also exclude opener-context single strokes | 31/59 | 324/539 | 0.8956 |

**The proposed set does not show the predicted enrichment.** Six alone is relatively frequent, but selecting it after seeing results cannot validate the full proposal. These p-values concern this enrichment statistic, not the probability Tamil is wrong. The test assumes numeral identifications, fish grouping, reading order, lexicon coverage, and exchangeable tokens; even distinct texts are not necessarily independent artifacts.

[Original script copy](provenance/tamil_stars.py) · [Complete reproduced output](provenance/tamil_stars-reproduced.md).

Other relevant repository entry points:

| Scripts | Local reproducibility constraint |
|---|---|
| `tamil_brahmi.py` | Requires external OCR `ete.txt`; descriptive comparison. |
| `predict_test171.py`–`175.py`, `197.py`, `198.py` | External Tamil/Brahmi/Prakrit and control name files under `LANG_DATA`; `ICIT_FULL` CSV also required. **198 withdraws 197’s language narrowing:** Japanese leads the genre-controlled comparison. |
| `predict_test179.py` | Bundled proposed keys permit partial A/B checks; complete run additionally needs Linear B, Yajnadevam, ICIT files. |
| `predict_test180.py`, `181.py` | External DEDR/lexicons or `CLICS4`; pooled Dravidian/world-language comparisons, not a Tamil decoder. |
| `predict_test206.py`, `207.py` | External lexicons and Linear B controls; uses pooled Dravidian, not Tamil alone. |

Source directory: `/tmp/indus-tamil-audit/targets/indus/`. Missing external datasets cannot be replaced silently: that would create a new experiment, not reproduce Bourdeau.
