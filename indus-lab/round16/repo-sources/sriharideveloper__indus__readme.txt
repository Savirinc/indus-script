<p align="center">
  <img src="assets/indus-lab.svg" alt="INDUS: evidence-first computational research on the Indus script" width="920">
</p>

# INDUS

**A falsifiable computational workbench for an undeciphered script.**

This repository asks what can be learned from sign order, repetition, archaeological metadata, and conservative external anchors without pretending that statistical labels are translations.

> **Bottom line:** the corpus contains strong, generalizable sequential structure. This project maps that structure and produces testable hypotheses. It does **not** recover the Harappan language, pronunciation, or literal readings.

## What is new here

The earlier experiment optimized *coverage*: it assigned one of five roles to every token. That was useful as an exploratory map, but easy to misread as “100% deciphered.” This release changes the center of gravity from coverage to falsifiability:

- exact duplicates are removed before model fitting;
- held-out strings never appear in training;
- four masked-sign models are compared against one another;
- normalized reading order is tested against exact reversal;
- every role label is observational rather than lexical;
- every headline has a denominator and an explicit forbidden interpretation;
- all 5,679 source rows, 3,219 analytic lines, and 12,910 token-level role assignments remain inspectable.

## Results at a glance

| Question | Result | What it establishes |
|---|---:|---|
| Can local context recover an unseen sign? | **26.1% top-1**, **50.9% top-5** | Reusable combinatorial constraints |
| Frequency-only baseline | 11.0% top-1, 24.2% top-5 | The context gain is substantial |
| Does a train-only model prefer normalized order? | **79.0%** of unseen eligible strings | Directional asymmetry generalizes |
| Do numeral-like signs precede the conservative measure-sign set? | **166 observed vs 67.4 shuffled**; empirical `p < 0.0005` | A strong quantity→measure association |
| Does sign identity carry positional information? | MI `0.368` nats vs null `0.071`; empirical `p < 0.001` | Signs have differentiated positional behavior |
| Can every token receive a structural slot hypothesis? | **100% annotation coverage** | A complete machine-readable role map, not complete decipherment |

The masked-sign scores are five-fold means on **2,082 unique complete strings**. Test tokens unseen in a fold's training vocabulary are reported as OOV and excluded from accuracy. Read [CLAIMS.md](docs/CLAIMS.md) before quoting a number.

![Masked-sign benchmark](results/figures/masked_sign_benchmark.svg)

## Corpus anatomy

- **5,679** source records and **3,219** complete, direction-known analytic line records
- **2,082** unique sign strings after exact deduplication
- **606** observed sign IDs and **9,311** tokens in the deduplicated corpus
- median string length **4**; maximum **13**
- **215** sign types occur once; **395** occur fewer than five times
- the 67 most frequent signs account for **76.1%** of deduplicated tokens
- **35.3%** of analytic line records duplicate another exact string
- **284** formulas repeat across artifacts and **77** across sites

These numbers are not incidental. They explain both why pattern induction works and why literal decipherment remains underdetermined.

## What the role map means

ACGI-5 assigns five deliberately modest structural labels:

```text
OPENING_SLOT → QUANTITY_LIKE → MEASURE_ASSOCIATED → CORE_SLOT → CLOSING_SLOT
```

The order is soft, not mandatory. The names describe distributional behavior. `OPENING_SLOT` does not prove “issuer”; `CORE_SLOT` does not prove “commodity”; `CLOSING_SLOT` does not prove “approval.” Those remain archaeological hypotheses.

```mermaid
flowchart TD
    A["Pinned secondary corpus"] --> B["Quality audit + direction normalization"]
    B --> C["Deduplicated structural tests"]
    C --> D["Held-out prediction benchmarks"]
    C --> E["Uncertainty-aware slot map"]
    D --> F["Claims with baselines"]
    E --> F
```

## Reproduce it

Python 3.11+ is recommended.

```bash
git clone https://github.com/sriharideveloper/indus.git
cd indus
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analysis/run_all.py
python analysis/verify_results.py
pytest -q
```

The full role model performs 24 bootstrap refits and can take several minutes. For the faster independent benchmarks:

```bash
python analysis/evaluate.py
```

To rebuild the reviewer notebook, install `requirements-dev.txt` and run `python analysis/build_notebook.py`.

Query a sign or exact sequence after generating results:

```bash
python analysis/query.py 740
python analysis/query.py 032-220
```

## Repository map

| Path | Purpose |
|---|---|
| [`analysis/`](analysis/) | corpus parsing, benchmarks, slot induction, contextual inference |
| [`data/DATA_CARD.md`](data/DATA_CARD.md) | provenance, inclusion rules, leakage and licensing |
| [`results/evaluation_summary.json`](results/evaluation_summary.json) | compact machine-readable benchmark summary |
| [`results/tables/`](results/tables/) | fold results, profiles, lexicon and complete role maps |
| [`reports/RESEARCH_NOTE.md`](reports/RESEARCH_NOTE.md) | results, interpretation, failure analysis and next experiments |
| [`docs/CLAIMS.md`](docs/CLAIMS.md) | claim ledger: allowed and forbidden interpretations |
| [`docs/METHODS.md`](docs/METHODS.md) | algorithms, splits, controls and known circularities |
| [`docs/RESEARCH_AGENDA.md`](docs/RESEARCH_AGENDA.md) | tests that could move this toward actual decipherment |

## Scientific stance

The strongest conclusion is not “we solved the Indus script.” It is:

> Sign order is predictable on held-out inscriptions, local context contains enough information to recover many hidden signs, and numeral-like signs have a robust directed association with a conservative measure-sign set. A five-slot model is a useful index over those regularities, but its English labels are hypotheses rather than translations.

This distinction is the project’s most important feature.

## Citation

See [`CITATION.cff`](CITATION.cff). The corpus snapshot is redistributed under its upstream MIT license with provenance and checksum; cite the upstream corpus and the primary studies listed in [SOURCES.md](docs/SOURCES.md).

## License

Code and original documentation are MIT licensed. The pinned secondary corpus retains its upstream MIT notice in [`data/raw/UPSTREAM_LICENSE`](data/raw/UPSTREAM_LICENSE).
