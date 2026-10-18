# Test your key

If you believe you have sign values for the Indus script, this is how to find out, in about twenty minutes, whether your readings carry your language or whether they are indistinguishable from a random re-assignment of your own values.

## 1. Write the key file

A tab-separated file with a comment header and one row per sign:

```
# My key, 2026. language: sa (Sanskrit) | ta (Tamil) | other. Source: ...
# sign	value	confidence	gloss
740	an	sure	jar sign = suffix -an
220	min	sure	fish = mīn
...
```

- `sign` is the ICIT catalogue number used in `indus-lab/raw/inscriptions.csv` (three digits; Mahadevan numbers must be converted first).
- `value` is the sound in any Latin transliteration; the harness collapses everything to one 21-letter alphabet (vowels a i u e o; consonants k g c j t d n p b m y r l v s), so diacritics and aspirates do not matter.
- `confidence` is `sure`, `likely` or `unsure`; you choose which tiers to test.
- Only the first two columns are scored. Glosses are for readers.

Minimum: 25 signs attested in the corpus. Below that the shuffle null has too few distinct permutations and the result is NOT TESTABLE. Coverage matters more than count: the Linear B control passes at about 60% token coverage and fails at 28%.

## 2. Register the key

Copy the file to `indus-lab/round49/keys/yourname.tsv` and add one line to the `KEYS` dictionary in `indus-lab/round49/run49.py`:

```python
 'YourName2026': (lambda: load_tsv_key('yourname.tsv', ('sure', 'likely')), 'Sanskrit', True),
```

The second element is the home language: `Sanskrit`, `Tamil`, `Finnish` or `Basque` are built in; adding another needs a lexicon of a few thousand words and a two-line loader in `load_lexicons()`.

## 3. Run

```sh
cd indus-lab/round47 && bash fetch_lexicons.sh      # pinned lexicons, once
cd ../round49 && python3 run49.py                    # standard library only
```

The log prints, for your key: the Linear B positive control at your coverage level; your home-language z and percentile against 1,000 structure-preserving shuffles of your own key; the same for Finnish, Basque and the cross-family language; and what a 60,000-step refit of your own values can reach in each language. The verdict word is printed last.

## 4. Read the verdict

| Word | Meaning |
|---|---|
| NOT TESTABLE | Fewer than 25 signs, or the Linear B control fails at your coverage. Nothing is concluded. |
| NULL | Your readings are not more like your language than shuffles of your own values (percentile < 0.95). |
| ARTEFACT | Your readings pass, but Finnish or Basque passes too, or the margin is under 2 sd. The fit is to word shape, not language. |
| MIXED | Something passed and something failed; the log says which clause. |
| SUPPORT | Percentile ≥ 0.99, z ≥ 3, and a margin of 2 sd over every other language, with the control passing. Then a pre-registered replication follows before anything is claimed. |

For reference, the real Linear B key scores z 11.5 at Indus density. Yajnadevam's key scores −0.35, Fairservis's 0.20, Rao's −0.70.

## 5. What the test does not do

It scores your key plus a mechanical reading rule. It does not score your manual glossing, segmentation, sandhi or dictionary choices, because those are where every published decipherment adds the language it then claims to have found. If your reading depends on that stage, freeze it as code so that Finnish gets the same freedom, and run that pipeline instead. The protocol for doing so is round 47's reopen criterion.

## 6. Tell us

Open a Discussion or Issue with your log. Results are added to `docs/STATUS.md` whatever they say.
