# Round 29 — Exact conditional-order test (pre-registered)

Written 11 October 2026 before any round-29 code was executed. Test material = the frozen round27 robustness splits (one-edit-excluded test types). These texts were already scored in rounds 27–28, so they are NOT a pristine holdout; this round asks a different question of them.

## Question
Round 28 left UNRESOLVED whether round27's bigram gain is explained jointly by (a) each inscription's sign composition and (b) length-specific slot preferences. Its swap sampler barely moved. This round avoids sampling: for every test inscription we condition on its exact sign multiset and enumerate all distinct orderings exactly.

## Models (all trained only on the source city; parameters fixed here)
- U: unigram (round27 `fit`). Order-invariant given the multiset ⇒ uniform over permutations. Reference floor.
- POS: P(x | L, i) for exact length L and slot i, interpolated with the round27 unigram, prior mass k=5: (c(L,i,x)+5·u(x))/(c(L,i)+5). Lengths unseen in training back off fully to u.
- BIG: round27 bigram model unchanged (BOS/EOS included).
- POS+BIG: log-linear product of POS and BIG sequence scores, equal weight 1, renormalised over the permutation set.

## Metric
For each test type s with multiset M, Perm(M)=distinct orderings. Conditional bits = −log2 [ score(s) / Σ_{p∈Perm(M)} score(p) ]. Report mean over test types, and the mean per-type difference.
Eligibility: |Perm(M)| ≥ 2 and length ≤ 9 (exact enumeration). Report how many types are excluded by each rule. Test-only signs map to UNK exactly as round27.

## Hypotheses and decision rule
- H_joint (round28 alternative): adjacency adds nothing beyond position+composition ⇒ POS+BIG not better than POS.
- H_adj: POS+BIG beats POS.
Primary statistic: mean(POS bits − POS+BIG bits) per condition, with a 95% bootstrap interval (2,000 resamples of test types, seed fixed).
- SUPPORT H_adj if the interval lies above 0 in at least 3 of 4 conditions, and in no condition lies below 0.
- SUPPORT H_joint if the interval includes or lies below 0 in at least 3 of 4.
- Otherwise MIXED.
Bootstrap treats types as exchangeable; related variants make the interval optimistic. It is descriptive.

## Negative control (validity of the metric)
For each condition, replace each test type's order with one ordering drawn from POS's own conditional distribution over Perm(M) (seeded). POS is then the true generating model, so POS+BIG should NOT beat POS. If the primary statistic's interval lies above 0 on this synthetic set in any condition, the metric is biased and the primary result is void.

## Positive control
Same procedure but draw the replacement order from BIG's conditional distribution. POS+BIG should beat POS. If not, the test has no power and a null primary result is uninformative.

## What a result can and cannot mean
Support for H_adj = sign adjacency carries information beyond composition and slot position that transfers across cities. That is consistent with linguistic writing AND with structured nonlinguistic systems (Sproat 2014). It assigns no sound, meaning, or language.
