# IndusBench v1.0

The first objective, reproducible benchmark for evaluating Indus Script decipherment models.

## Why IndusBench?

Indus Script decipherment has been debated for over a century. Claims and counterclaims are argued subjectively — "this sign looks like that Brahmi letter," "this reading makes sense in Sanskrit." IndusBench replaces subjective debate with reproducible measurement: **train on 80% of the corpus, predict the held-out 20%, and score with quantitative metrics.**

## Quick Start

```bash
# Enter nix shell (provides uv + python)
nix-shell -p uv

# Create venv and install deps
uv venv && source .venv/bin/activate
uv pip install mlx numpy scikit-learn

# Download large data files (Sumerian ATF + CDLI catalogue)
# These are excluded from git due to size (>100MB)
./download_data.sh

# Run the full benchmark
python run_benchmark.py

# Run 5-fold cross-validation
python run_cv.py

# Run cross-script calibration (Indus vs Linear B vs Sumerian)
python cross_script/run_cross_script.py
```

## What It Does

```
Phase 1: Corpus        →  3,237 unique inscriptions, 712 signs, 68 sites
Phase 2: Normalization →  716 sign variants mapped to canonical forms
Phase 3: Split         →  2,664 train / 573 test (stratified by site/type/class)
Phase 4: Lock          →  SHA256 checksums prevent test-set peeking
Phase 5: Evaluate      →  7 models × 6 metrics → DCS composite score
```

## Leaderboard

### Single Split (Locked Test Set)

| Rank | Model | DCS | Next-Sign Acc | BPS | Entropy Red. | Grammar |
|------|-------|-----|---------------|-----|--------------|---------|
| 1 | **Yajnadevam** | **43.8** | 16.6% | 4.91 | 27.7% | 0.65 |
| 2 | Markov-3gram | 39.2 | 17.1% | 6.38 | 5.0% | 0.66 |
| 3 | Markov-2gram | 38.9 | 14.4% | 6.35 | 5.7% | 0.66 |
| 4 | Transformer-MLX | 37.4 | 10.1% | 5.64 | 24.0% | 0.65 |
| 5 | Frequency | 34.3 | 1.5% | 7.44 | 0.0% | 0.65 |
| 6 | Random | 30.5 | 0.6% | 9.48 | 0.0% | 0.69 |
| 7 | HMM | 29.2 | 8.2% | 9.85 | 0.0% | 0.65 |

### 5-Fold Cross-Validation

| Rank | Model | DCS (mean ± std) | Next-Sign Acc | BPS | Entropy Red. |
|------|-------|-------------------|---------------|-----|--------------|
| 1 | **Yajnadevam** | **43.9 ± 0.8** | 17.0 ± 1.8% | 4.89 ± 0.10 | 0.279 ± 0.014 |
| 2 | Markov-3gram | 39.0 ± 1.0 | 17.6 ± 1.6% | 6.39 ± 0.14 | 0.045 ± 0.022 |
| 3 | Markov-2gram | 38.7 ± 0.8 | 14.7 ± 1.7% | 6.36 ± 0.13 | 0.054 ± 0.020 |
| 4 | Transformer-MLX | 37.4 ± 1.1 | 12.2 ± 1.3% | 5.68 ± 0.22 | 0.239 ± 0.024 |
| 5 | Frequency | 34.0 ± 0.4 | 0.6 ± 0.2% | 7.49 ± 0.12 | -0.084 ± 0.022 |
| 6 | HMM | 31.1 ± 2.8 | 9.7 ± 0.8% | 10.74 ± 4.50 | -0.671 ± 0.629 |
| 7 | Random | 30.5 ± 0.2 | 0.5 ± 0.2% | 9.48 ± 0.00 | -0.342 ± 0.005 |

## DCS: Decipherment Confidence Score

Composite score in [0, 100]:

```
DCS = 0.20 * Prediction   (next-sign + missing-sign accuracy)
    + 0.20 * Compression   (bits-per-symbol vs random baseline)
    + 0.15 * Entropy       (entropy reduction over unigram model)
    + 0.15 * Grammar       (bigram repeatability + positional entropy + model ranking)
    + 0.10 * Context       (object-type prediction improvement over majority baseline)
    + 0.10 * Reproducibility (deterministic = 1.0)
    + 0.10 * Simplicity    (Occam's razor: fewer params = higher score)
```

## Six Metrics

1. **Prediction Accuracy** — Given a sign sequence prefix, predict the next sign. Also: given a sequence with one sign masked, predict the missing sign. Top-1 and Top-5 accuracy.

2. **Sequence Probability** — Average log-likelihood of held-out sequences under the model. Measures how well the model's internal probability distribution matches the true distribution.

3. **Compression (BPS)** — Bits per symbol using arithmetic coding with the model's predicted distribution. Lower = better. Random baseline = log2(712) = 9.48 BPS.

4. **Entropy** — Unigram entropy H1, bigram conditional entropy H2|H1, trigram H3|H2, and model cross-entropy. Entropy reduction = (H1 - model_cross_entropy) / H1. Higher = better.

5. **Grammar Consistency** — Three sub-metrics:
   - *Bigram repeatability*: fraction of test bigrams that also appear in training (corpus-level grammar)
   - *Positional entropy reduction*: how much knowing position constrains which signs appear
   - *Model ranking*: for each test bigram (A,B), does the model rank B in the top percentile given context A?

6. **Context Prediction** — Can sign sequences predict archaeological context (object type)? Uses k-NN on model log-probabilities. Baseline = majority class. Score = max(0, accuracy - baseline).

## Models

| Model | Description | Key Idea |
|-------|-------------|----------|
| Random | Uniform distribution over signs | Lower bound |
| Frequency | Unigram distribution | Most common sign always |
| Markov-2gram | Bigram model with Kneser-Ney smoothing | P(next \| prev) |
| Markov-3gram | Trigram model with Kneser-Ney smoothing | P(next \| prev2, prev1) |
| HMM | 20-state Hidden Markov Model | Latent state structure |
| Transformer-MLX | 4-layer, 128-dim, 4-head transformer on Apple Silicon GPU | Attention-based sequence model |
| **Yajnadevam** | Phoneme-level n-gram blended with sign-level n-gram | Uses S. Jeyakumar's sign-to-phoneme mapping from [lipi](https://github.com/yajnadevam/lipi) |

## Corpus

- **Source**: `lipi/src/assets/data/inscriptions.csv` from [yajnadevam/lipi](https://github.com/yajnadevam/lipi)
- **Size**: 3,237 unique inscriptions (deduplicated from 5,679 rows)
- **Vocabulary**: 712 unique signs (normalized from 716 variants via `xlits.csv`)
- **Sites**: 68 archaeological sites
- **Average length**: 3.95 signs per inscription
- **Long-tailed**: Top 10 signs cover ~50% of all sign occurrences

### Normalization

Signs are normalized using the `xlits.csv` mapping:
- 96 canonical signs
- 214 composite signs (ligatures)
- 13 variant groups (allographs collapsed)
- 78 signs with phoneme assignments (from `decipher.csv`)

### Split

Stratified 80/20 split by (site, object_type, class):
- 2,664 training inscriptions
- 573 test inscriptions (locked with SHA256 checksums)
- 45 test-only signs unseen in training (inherent to long-tailed distribution)
- 5-fold cross-validation splits also available for robust evaluation

## Directory Structure

```
indus-bench/
  corpus/
    build_corpus.py       # Phase 1: gold corpus builder
    inscriptions.json     # 3,237 unique inscriptions
    sign_inventory.json   # 712 signs with frequencies
  normalization/
    build_normalization.py  # Phase 2: sign normalization
    sign_map.json           # canonical map, variants, phonemes
  split/
    build_split.py     # Phase 3-4: split + lock
    train.json         # 2,664 training inscriptions
    test.json          # 573 test inscriptions (locked)
    lock.json          # SHA256 checksums
    cv_folds.json      # 5-fold CV splits
  baselines/
    base_model.py          # abstract model interface
    models.py             # Random, Frequency, Markov, HMM
    mlx_transformer.py    # MLX transformer (Apple Silicon GPU)
    yajnadevam_model.py   # phoneme-level n-gram model
  evaluation/
    metrics.py         # 6 metrics + DCS composite
  results/
    benchmark_results.json  # full detailed results
    leaderboard.csv          # sorted leaderboard
    cv_results.json         # cross-validation results
    cross_script_results.json # cross-script calibration data
  cross_script/
    parse_linear_b.py       # Linear B corpus parser
    parse_sumerian.py       # Sumerian cuneiform parser
    run_cross_script.py     # cross-script benchmark runner
    data/                   # parsed corpora + raw sources (see download_data.sh)
  run_benchmark.py    # main runner
  run_cv.py           # cross-validation runner
  shell.nix           # nix shell
```

## How to Add Your Model

1. Create a model class that inherits from `BaseModel`:
```python
from baselines.base_model import BaseModel

class MyModel(BaseModel):
    def __init__(self):
        super().__init__("MyModel")

    def train(self, train_data):
        # Train on list of inscription dicts
        # Each has: id, site, object_type, sign_sequence (list of sign IDs)
        pass

    def predict_next(self, context):
        # Given list of preceding signs, return {sign_id: probability}
        pass

    def sequence_logprob(self, sequence):
        # Return log P(sequence) under the model
        pass

    def bits_per_symbol(self, sequence):
        # Return BPS = -log2(P(sequence)) / len(sequence)
        pass
```

2. Add it to `models_config` in `run_benchmark.py`:
```python
("MyModel", lambda: MyModel()),
```

3. Run: `python run_benchmark.py`

## Key Findings

### Within-Script (Indus Only)

1. **Yajnadevam wins** (43.9 DCS in CV) — the phoneme mapping provides structural knowledge that pure statistical models can't learn from 2,664 short sequences.

2. **Markov-3gram wins on raw prediction** (17.6% next-sign accuracy) but loses on compression and entropy. It memorizes specific bigrams but doesn't learn the underlying distributional structure.

3. **Transformer-MLX excels at compression** (5.68 BPS, 2nd best) and entropy reduction (23.9%) but underperforms on raw prediction (12.2%). With only ~10K training tokens, it learns structure but can't memorize specific sequences.

4. **Context prediction fails for all models** — sign sequences don't predict object type above majority baseline (49%). This suggests either (a) the script is not context-dependent, or (b) object type is too coarse a label.

5. **HMM is unstable** (31.1 ± 2.8 DCS) — high variance across folds, sometimes worse than random. The 20-state HMM is too complex for this corpus size.

6. **Grammar is corpus-level** — bigram repeatability (69.8%) and positional entropy reduction (23.5%) are the same for all models. Only model ranking differentiates. This means the corpus has inherent grammar, but all reasonable models pick it up equally.

### Cross-Script Calibration

We ran the same benchmark on **Linear B** (deciphered syllabary, 4,193 inscriptions, 104 signs) and **Sumerian cuneiform** (deciphered logo-syllabic, 5,000 inscriptions, 5,852 signs), with sequences truncated to 5 signs for fair comparison.

#### Corpus-Level Entropy (Matched, first 5 signs)

| Script | Type | Signs | H1 (bits) | H2\|H1 (bits) | Entropy Reduction |
|--------|------|-------|-----------|----------------|-------------------|
| **Indus** | Undeciphered | 644 | 6.95 | 2.97 | **57.2%** |
| Linear B | Syllabary | 103 | 5.91 | 3.54 | 40.0% |
| Sumerian | Logo-syllabic | 1,236 | 7.76 | 2.59 | 66.7% |

**Key finding**: Indus has *stronger* bigram structure than Linear B. Knowing the previous sign reduces uncertainty by 57.2% for Indus vs only 40.0% for Linear B. The script is not random — signs are strongly constrained by their neighbors.

#### Model Performance (Markov-3gram, matched)

| Script | DCS | Pred% | BPS | Entropy Red. | Bigram Repeat |
|--------|-----|-------|-----|--------------|---------------|
| Indus | 38.3 | 15.7% | 6.37 | 4.4% | 69.2% |
| Linear B | 43.9 | 24.9% | 5.10 | 12.7% | 90.2% |
| Sumerian | 48.1 | 43.9% | 5.60 | 27.8% | 75.9% |

Models perform worst on Indus despite it having strong corpus-level structure. This is a **data sparsity problem**: 644 signs with ~9,000 training tokens means most bigrams are unseen. Linear B (103 signs) has far better coverage.

#### Yajnadevam's Phoneme Mapping vs Sumerian

| Model/Script | Entropy Reduction |
|--------------|------------------|
| Indus Markov-3gram (sign-level) | 4.4% |
| Indus Yajnadevam (phoneme-level) | 27.1% |
| Sumerian Markov-3gram (sign-level) | 27.8% |

Yajnadevam's phoneme mapping achieves 27.1% entropy reduction — remarkably close to what Markov-3gram achieves on Sumerian (27.8%), a fully deciphered script. The mapping appears to be capturing genuine linguistic structure that sign-level models miss due to data sparsity.

#### Conclusions

1. **Indus has structure consistent with language** — bigram entropy reduction of 57.2% is higher than Linear B (40.0%) and approaches Sumerian (66.7%). Non-linguistic symbol systems would not show such strong sequential constraints.

2. **Indus behaves more like a logo-syllabic script than a syllabary** — high sign inventory (712 signs), high unigram entropy (7.08 bits), and strong bigram constraints (57.2% reduction) match the Sumerian profile more than the Linear B profile.

3. **The bottleneck is data, not structure** — the Indus corpus has strong sequential structure, but models can't learn it because 712 signs × 3,237 short inscriptions = severe data sparsity. With more data (or a better inductive bias like phoneme mappings), models should perform better.

4. **Yajnadevam's mapping is structurally meaningful** — it captures structure at a level comparable to what statistical models achieve on deciphered Sumerian. This doesn't prove the decipherment is correct, but it shows the mapping is not arbitrary.

## Technical Notes

- **Apple Silicon GPU**: Transformer runs on MLX with `mx.set_default_device(mx.gpu)`. Training takes ~16s for 80 epochs on M-series chips.
- **Reproducibility**: All models use fixed random seeds. Test set is locked with SHA256 checksums in `split/lock.json`.
- **Corpus size**: 3,237 inscriptions × 3.95 signs avg = ~12,800 tokens. This is tiny by NLP standards — models are megabytes, not gigabytes.
- **No external data**: All models train only on the Indus corpus. No transfer learning, no pretrained embeddings.

## Data Sources

The Indus corpus is built from [yajnadevam/lipi](https://github.com/yajnadevam/lipi) and is included in `corpus/`.

Two large raw data files for cross-script calibration are excluded from git (they exceed GitHub's 100MB limit). The processed JSON files are included, so you only need these if you want to re-run the parsing:

| File | Size | Source | Used By |
|------|------|--------|---------|
| `cross_script/data/cdliatf_unblocked.atf` | 83 MB | [CDLI](https://cdli.ucla.edu) — download from [here](https://cdli.ucla.edu/files/cdliatf_unblocked.atf) | `parse_sumerian.py` |
| `cross_script/data/cdli_cat.csv` | 148 MB | [CDLI](https://cdli.ucla.edu) — download from [here](https://cdli.ucla.edu/files/cdli_cat.csv) | `parse_sumerian.py` |
| `cross_script/data/LinearBInscriptions.js` | 10 MB | [Packhum](https://packhum.org) | `parse_linear_b.py` |

Run `./download_data.sh` to fetch the CDLI files automatically. The processed outputs are already included:

- `cross_script/data/linear_b_corpus.json` (2.4 MB) — 4,193 Linear B inscriptions
- `cross_script/data/sumerian_corpus.json` (6.5 MB) — 5,000 Sumerian cuneiform inscriptions

For the Panini grammar test, [vidyut](https://github.com/avinashvarna/vidyut) requires its kosha (lexicon) data at `~/.vidyut-data/kosha/`. Install via:
```bash
pip install vidyut
# Download kosha data (167M forms, ~1GB):
python -c "import vidyut; vidyut.kosha.download()"
```



```
mlx                    # Apple Silicon GPU acceleration
numpy                  # numerical computation
scikit-learn           # KNN for context prediction metric
```

## References

- Corpus source: [yajnadevam/lipi](https://github.com/yajnadevam/lipi) — S. Jeyakumar's Indus script database
- Sign normalization: Based on `xlits.csv` canonical mapping
- Phoneme mapping: Based on `decipher.csv` sign-to-Sanskrit phoneme assignments
- Cross-validation: 5-fold stratified splits, each fold tested once

## License

Same as source corpus (yajnadevam/lipi).

---

*IndusBench v1.0 — Replace subjective decipherment debates with reproducible measurement.*
