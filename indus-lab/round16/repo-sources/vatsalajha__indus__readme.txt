<h1>Indus Engine</h1>

<p>
<a href="https://vatsalajha.github.io/indus/"><img alt="Interactive site" src="https://img.shields.io/badge/interactive_site-live-2E6D64"></a>
<img alt="License MIT" src="https://img.shields.io/badge/license-MIT-blue">
<img alt="Python 3.12" src="https://img.shields.io/badge/python-3.12-3776AB">
<img alt="Deterministic" src="https://img.shields.io/badge/results-deterministic_(seed_7)-555">
<img alt="No decipherment claimed" src="https://img.shields.io/badge/phonetic_values_assigned-zero-A84927">
</p>

**Nobody can read the Indus script. This project does not claim to.**

It asks a narrower question that can actually be answered: given only raw
sequences of signs, with no sign meanings, no positional information and no
linguistic assumptions, can a computer recover how the script is *organised*?

It can. An unsupervised method rediscovers the functional sign classes that
scholars established by hand in the 1970s, and those machine-found classes then
correctly predict sign behaviour in a much larger catalogue compiled decades
earlier by a different scholar in a different notation.

**No sound is assigned to any sign anywhere in this work.** Where the evidence
stops is marked as carefully as where it reaches.

### → [Play the evidence](https://vatsalajha.github.io/indus/)

Build an inscription and watch it collapse when shuffled. Try to read a sign
inventory where half the signs appear once. Watch a tempting decipherment get
broken on purpose. Same numbers as this repository.

---

## Three numbers

| | result | control | significance |
|---|:--:|:--:|---|
| Five-slot grammar parses the primary corpus | **75.4%** | 23.0% shuffled | p < 0.001, 1,000 permutations |
| Replicates on a corpus 14× larger | **71.4%** | 27.3% shuffled | p < 0.001, different numbering system |
| Induced suffix class is text-final in Mahadevan's 13,372 occurrences | **0.632** | 0.223 baseline | p < 0.0001, frequency-matched |

The jar and lance signs pair at cosine **0.831** on neighbour context alone,
with no positional information supplied. That is Mahadevan's terminal class,
recovered blind.

## What survived, and what this project broke itself

Seven claims survive. Two were wounded by our own tests, two are honest nulls,
two were withdrawn against gold-standard data, and the large secondary corpus is
only partially verified.

![Integrity scorecard: every claim marked by whether it survived our own falsification](results/figures/figD_scorecard.png)

Including the one everyone wants to be true: Parpola's *mīn* pun, where "fish"
and "star" are homophones in Dravidian, is real and checkable in the
etymological dictionary. But numeral-plus-fish groups sit bare in mid-text like
items in a tally, not like named entities. **The pun survives. The reading does
not.** Of thirteen signs whose pictogram is confidently identifiable, **zero**
earn a phonetic rebus that survives a frequency-matched null model.

## Quickstart

```bash
git clone https://github.com/vatsalajha/indus && cd indus
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python run.py     # gates → analyses → number check → figures
```

In a bare clone this runs cleanly and reports `SKIP` for every stage that needs
the corpus, with the reason. **Skipped is never counted as passed.** With the
corpus regenerated per [`DATA.md`](DATA.md), the same command reproduces every
shipped number exactly: seeded throughout, dependencies pinned to the versions
that produced `results/`.

[`REPRODUCIBILITY_REPORT.md`](REPRODUCIBILITY_REPORT.md) documents a fresh-clone
audit and the five blockers it found.

## Repository map

```
src/analysis/    the statistical attacks, one file per question
src/parse/       extraction from the source publications (no corpus data inside)
src/figures/     figure generation
results/         aggregate statistics and figures — the shipped evidence
tests/           validation gates + a gate asserting the paper's numbers
docs/            the interactive site (GitHub Pages)
run.py           the whole pipeline, one command
```

## Data: what is here and what is not

**Ships:** all analysis code, all extraction code, aggregate statistics,
figures, validation gates, the site.

**Does not ship: any row-level corpus data.** The corpora derive from
copyrighted publications, and redistributing the transcriptions would
redistribute the copyrighted expression.

| corpus | status |
|---|---|
| 179 CISI unicorn seals (primary) | MIT-licensed third-party digitization — clone it yourself, not re-hosted here |
| Fuls, *Corpus of Indus Inscriptions* | copyrighted, extraction procedure documented |
| Mahadevan 1977 Table I | copyrighted expression, dual-checksum validation documented |
| ICIT 2,511-seal compilation | third party, factual sequences only |

What this repository publishes instead of the data is **the procedure, and the
gates a correct reproduction must pass** — the part that makes the result
checkable. [`DATA.md`](DATA.md) covers all ten required files and which script
produces each.

## How to challenge this

The method is built to be beaten. That is the point of shipping it.

1. **Beat the benchmark.** The template test, the frequency-matched permutation
   test against Table I, and the rebus null model are all in `src/analysis/`.
   Any decipherment claim can be asked to pass them. None tested so far does.
2. **Attack the numeral list.** The most list-sensitive finding here.
   `src/analysis/redteam.py` already tests three definitions, strict to
   deliberately over-inclusive; the fish share holds between 0.20 and 0.27.
   Propose a fourth.
3. **Falsify the stated prediction.** Table I contains frequent, strongly final
   signs the induced suffix class does *not* include — Mahadevan's 176, 328 and
   12. On a corpus large enough to sample them, they should join the jar-lance
   cluster unsupervised. If they do not, the method measures something narrower
   than claimed.
4. **Break the reproduction.** If `run.py` does not regenerate the shipped
   numbers on your machine, open an issue.

## Citing

See [`CITATION.cff`](CITATION.cff). The software and the preprint are cited
separately: the preprint is the claim, the software DOI is the thing that
reproduces it. Both DOIs to be added on deposit.

## AI-assistance disclosure

Anthropic's Claude, used through Claude Code, served as a programming and
writing aid under the author's direction: extraction tooling, analysis and
testing code, figure generation, drafting support. No AI tool is an author or
can bear responsibility for this work. The author designed the study and its
pre-registered scoring criteria, verified all transcriptions against the primary
sources, checked all computational outputs, and takes full responsibility for
the content, including any errors. Every statistic is produced by the
deterministic seeded scripts here; none is generated or paraphrased by a
language model.

## Licence

Code and aggregate results: MIT, see [`LICENSE`](LICENSE). Corpus data is not
included and is not covered by this licence.
