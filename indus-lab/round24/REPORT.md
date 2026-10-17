# Copper tablets: test and source check

11 October 2026. No phonetic value or translation established.

## What was executed

The script reads a strict field whitelist from the supplied inscription CSV, excluding its Sanskrit and translation columns. There are 237 copper-tablet rows representing 185 catalogue object IDs. Requiring an informative, unambiguous motif category and a clean directed inscription leaves 61 objects in 23 exact-text families. 112 objects lack an unambiguous informative motif under the protocol; 12 more lack a clean directed text. This subset is not the whole corpus.

| Test | Correct | Predictions made | All eligible objects | Equal-family mean success |
|---|---:|---:|---:|---:|
| Hold out one object, look up identical texts | 45 | 46 | 61 | 39.1% |
| Hold out every identical text, use nearest remaining family | 15 | 26 | 61 | 21.7% |

Abstentions are retained as unsuccessful cases in overall accuracy. The first test achieves 45/61 overall, the second 15/61. Correct/predicted accuracy is a different denominator: 45/46 and 15/26 respectively. Neither test is an independent archaeological validation. For 26 objects, holding out the text family removes their motif category from training altogether, so a closed-label nearest-family predictor cannot get those cases right. The majority baseline has zero correct predictions under these splits; this is a consequence of the dataset/splits, not evidence of semantic decipherment.

## Apparent counterexample, then primary-source correction

The CSV assigns exactly the same stored sequence, 407–061–845–240–798, to M-567 (Gaur), M-568 (Tigr) and M-1517 (Tigr). This initially looks like one text associated with different animals. We did not promote that observation to a semantic conclusion.

The published plates were then inspected directly:

- CISI1 printed142/PDF178 contains M-565–568 and is headed `comp. an. III, IV`.
- CISI2 printed217/PDF252 contains M-1515–1518 and is headed `composite animal III`.

These headings classify the plate groups as composite animals, whereas the CSV categories imply ordinary animal labels. They do not by themselves prove identical subtypes for all three objects. The scans show animal motifs but do not independently certify every sign of the supposedly shared text. Publication highlighting/tracing and poor preservation further limit a stroke-level comparison.

Decision: flag all three database motif labels as requiring source reconciliation before using this family to test an animal-name reading. Preserve the CSV unchanged. Do not assert either a genuine gaur-versus-tiger counterexample or a corrected exact animal identity from this check alone. The apparent contradiction is not currently a reliable semantic constraint.

## Another visible catalogue pattern

All 11 eligible Elep-labelled objects belong to two related stored sequences: four use 001–740–923–033–706 and seven use 740–923–033–706. Their mutual nearest-family predictions therefore exploit a one-sign prefix difference. This explains 11 of the 15 successful family-holdout predictions. It is a useful group to audit photographically, not 11 independent demonstrations that a reading generalises. The ID 001 is a catalogue sign ID, not an asserted numeral value. No translation follows.

## Research decision

The catalogue supports repeated associations but its animal labels cannot yet serve as trusted linguistic targets. Before combining these records with ancestral Dravidian roots, construct a source-checked motif ledger that separates visible features, publisher classification, database label and proposed meaning. Begin with the flagged three-object family and the eleven-object Elep group. Store uncertain sign positions and motif identifications explicitly; never fill them from a proposed reading.

A valid next constraint would be independently legible paired faces, consistent source classification and a prediction made before examining the test objects. This round does not provide that independent constraint; it identifies why the candidate counterexample is insufficient and preserves a reproducible audit.

## Limits and reproduction

Exact-string families can retain near-duplicates, aliases and shared production history across folds. Stored orientation is not canonicalised. One database category may contain heterogeneous pictures. Selected face provenance can be recovered by matching object/text in copper_source_ledger.json, but the prediction rows do not identify a unique face when multiple rows share that text. No statistical independence is asserted.

Run `python indus-lab/round24/test_motifs.py` from the extracted archive root. Source hash, exclusions, all predictions and whitelisted copper records are included. Source data and original licence accompany the code. The selected publication pages and their provenance are in plates/ and plate_provenance.json.
