# Round 59: If the Brahmi-based key were right, would the seals name the goods we know were traded? (pre-registered)

Written 24 October 2026, before `run59.py` exists and before any lexicon was matched against any Indus reading. Disclosed in advance:
- the lexicon files below were built and skimmed for format (samples printed);
- round 57 used the same matching instrument for place names (NULL), and round 47 its language-model test (NULL) on the same key.

## Question
Trade is the most solid history we have about the Indus people. Lapis came from Afghanistan and carnelian from Gujarat, and Mesopotamia received carnelian, ivory, fine wood, gold and exotic animals from Meluhha. Seals were used in trade. So, **assume the Brahmi-derived key (Yajnadevam's, round 46 expanded map) is right. Do the seal readings contain words for traded goods more often than chance**, either in Sanskrit or in Proto-Dravidian?

The key is read as a consonant skeleton (round 47 `read_c`, round 57 matching rule). Brahmi was used for both Indo-Aryan and Tamil, and a consonant skeleton ignores the vowels where the two would differ. So the same reading is tested against both lexicons, which gives neither language an advantage. Bhaty's change (435/436 → o) changes only a vowel and so leaves the skeleton unchanged; her variant is covered.

## Ledger status (rule 4)
**Scored test, cluster K7** (published phonetic keys; same key and instrument as rounds 47 and 57).
- **SUPPORT** in either lexicon → K7 is re-scored at **×3 toward L∪R jointly versus N**. Weak, because this key has already failed rounds 47 and 57, and two lexicons are tried, so the model-hunting discount applies (rule 8).
- **Any other outcome** → **no update**. A null for one key is about as likely under L or R as under N (K7 reasoning).

The gate passes, since one outcome can move a hypothesis by ×3.

## Lexicons (frozen with this protocol; built by `build59.py` from fixed rules)
Commodity keywords, fixed now, matched as whole words, case-insensitive: carnelian, cornelian, agate, lapis, beryl, crystal, gem(s), jewel(s), precious stone, bead(s), pearl(s), coral, shell, conch, ivory, elephant, tusk, gold, silver, copper, bronze, tin, metal, bitumen, wood, timber, ebony, rosewood, sandal, sandalwood, ship, boat, cotton, cloth, garment, wool, sesame, barley, wheat, rice, grain, oil, ghee, butter, honey, salt, peacock, monkey, dog, cow, cattle, bull, ox, buffalo, goat, sheep, ram, merchant, trade, price, weight.

| File | Language | Rule | Entries |
|---|---|---|---:|
| `lex_skt_commodity.tsv` | Sanskrit | DCS dictionary lemma whose first sense contains a keyword | 5,057 |
| `pool_skt_other.tsv` | Sanskrit decoy pool | all other DCS lemmas | 175,075 |
| `lex_pdr_commodity.tsv` | Proto-Dravidian (the stage nearer 2500 BCE than Tamil; X6) | pdr_04 reconstruction whose meaning contains a keyword | 874 |
| `pool_pdr_other.tsv` | Proto-Dravidian decoy pool | all other reconstructions with a meaning | 13,124 |
| `lb_commodity_rows.tsv` | Linear B (control) | words whose Greek equivalent is one of 44 fixed commodity lemmas (gold, silver, bronze, lead, oil, wine, honey, barley, wheat, linen, sesame, cumin, celery, ivory, horn, ox, sheep, goat, pig, horse, tunic, axe, swords, cup, amphora, ointment, seed, blue glass, drug, …) | 26 |

The lexicons are noisy by design. "Name of a merchant" counts because it contains *merchant*, and "to split wood" counts because it contains *wood*. Fixed rules, with no hand-picking, are what make the decoys fair.

## Procedure
1. **Corpus and readings.** Corpus, key, readings, skeleton rules and the statistic T are those of round 57, unchanged:
   - corpus: `R.load_corpus()`, texts whose signs all have values;
   - reading: `read_c`; skeleton: `merged_skel`;
   - words: only skeletons of three or more consonants;
   - T = number of distinct (text, skeleton) matches.
2. **Null.** 1,000 structure-preserving key shuffles (round 47 frequency bins), seeds 59201–60200. Reported: z and percentile of the real key's T among the shuffles.
3. **Decoys (on the real key only).** Each draw is the same size as the lexicon and matched to its skeleton-length distribution:
   - (a) **scrambled:** each commodity skeleton with its consonants shuffled (round 57 `scramble`), 20 draws, seeds 59501–59520;
   - (b) **ordinary words:** skeletons drawn at random from the same language's decoy pool, excluding commodity skeletons, 20 draws, seeds 59601–59620.
   - Per-word rate = T / number of skeletons.
4. **Positive control.** Linear B at Indus density, using round 57's PC2 geometry (seed 47301 half split, `lb_build`) and the true key. The lexicon is the 26 Linear B commodity words in Linear B spelling, skeletons of three or more consonants. It passes if all of these hold:
   - T ≥ 5;
   - percentile ≥ 0.99 and z ≥ 3 against 1,000 key shuffles (seeds 59201–60200);
   - commodity per-word rate above the 95th percentile of scrambled decoys (a).
   - The ordinary-word decoy (b) cannot apply to the control, because every Linear B word is in the control texts by construction.
   - If the control fails, the round is **VOID**, with Indus results reported only as description.

## Verdict per lexicon (Sanskrit, Proto-Dravidian), fixed now
| Verdict | Condition |
|---|---|
| **SUPPORT** | percentile ≥ 0.99 and z ≥ 3, and per-word rate above the 95th percentile of **both** decoys (a) and (b) |
| **WORDS, NOT GOODS** | percentile ≥ 0.99 and z ≥ 3, above decoy (a) but not above (b): words in general match, goods specifically do not |
| **ARTEFACT** | percentile ≥ 0.95 but not above decoy (a) |
| **NULL** | percentile < 0.95 |
| **MIXED** | anything else |

**Robustness (rule 7):** if z lies in 2.5–3.5 with percentile ≥ 0.99, the shuffle null is redrawn 10 times (10 × 1,000 shuffles, seeds 61001+), and SUPPORT stands only if ≥ 8 of 10 also give z ≥ 3.

**Description only:** the 25 most-matched commodity skeletons for each lexicon, with their glosses.

## Files
`PROTOCOL.md`, `build59.py` and the five lexicon files (committed together; PROTOCOL `chmod 444`), then `run59.py` (`chmod 444`, sha256 in commit), `results.json`, `run59.log`, `REPORT.md`. Afterwards: a STATUS row and a ledger K7 row.
