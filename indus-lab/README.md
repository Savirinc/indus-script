# Indus evidence lab — first runnable build

Run `python3 run.py` from any directory. Python 3 standard library only. The input snapshot and outputs are supplied. Run `python3 index_book.py PATH_TO_PDF` to index a locally obtained book; this optional command needs PyMuPDF. The index is page-level retrieval assistance, not a verified transcription of the illustrations.

## What the system does now

- Preserves the 2,543 source rows without assigning sound values, expanding compound signs, or changing motif labels.
- Creates a queryable SQLite database of objects and their lines, preserving catalogue identifiers and source fields.
- Groups exact full-object sequences, retaining line boundaries; reports copies, sites, types, motifs and all associated object IDs.
- Counts repetition separately by source object category.
- Generates equal-length, single-sign substitutions among complete one-line texts of 3–12 signs.
- Replicates one known positional observation with 999 randomizations and a fixed seed, counting each distinct eligible line once.
- Includes empty image/sign-region tables for further image annotation. Five photographed views have been visually inspected separately in `image_review.json`; these are observations, not verified sign transcriptions or a training set.

## Evidence architecture

Source file → page/view → physical object → face → sign occurrence → alternative transcription → sequence/context → test → hypothesis.

An object can have many photographs. A seal impression is a view or a related object, not automatically another seal. A modern impression is not an ancient find. A sign-list identifier is not a word. A shared sequence does not prove a shared physical object. Exact-text collapse is a sensitivity analysis, not archaeological deduplication.

The `image_views`, `sign_occurrences`, and `hypotheses` database tables provide the next annotation layer; automatic image segmentation, image registration and a trained recognition model are NOT implemented in this version.

## How picture comparison should work

1. Link every view to its source page and physical-object identifier; record ancient surface, photograph, modern impression, tracing, or reconstruction.
2. Keep the original scan immutable. Put cropping, mirroring, contrast changes and registration in separate derived records with coordinates and transformation history.
3. Extract sign occurrences as alternatives, recording damage and uncertainty. Use topology (strokes, junctions, enclosures), then geometric similarity; do not infer identity from silhouette alone.
4. Compare candidate variants within the same sequence position and object class. Overlay only after scale/orientation alignment; an overlay is a comparison, not proof that two objects fit together.
5. For fragments, require complementary edges, material, thickness, scale and archaeological plausibility before proposing a physical join. Visual resemblance alone is insufficient.

## Tests to pursue next

- **Minimal substitutions:** does replacing one sign repeatedly accompany a particular change in picture/context? Compare within site, type, length and preservation; permute labels only within valid matched groups. Report missing labels and ambiguous sign readings.
- **Picture/text coupling:** does the same text retain the same independently annotated motif across distinct objects and sites? Compare raw objects, exact-text groups, and suspected production batches.
- **Variant versus distinct sign:** do two similar shapes occur interchangeably in the same contexts, or do their neighbours differ? Keep a split and a merged model and compare out-of-sample prediction.
- **Time:** fit directional change only where independently dated contexts exist. Modern visual resemblance cannot date an inscription.
- **Meaning:** register a proposed reading and explicit predictions before checking held-out material. Compare at least one competing explanation. A successful structural test is not a translation.

The initial run is exploratory. Its inputs have already been examined in the source project, so a random train/test split cannot make these observations independent discoveries. Later confirmation should hold out object families, sites and independent transcription work, with sign mappings learned only from training data. Apply multiplicity correction to any large scan of associations.

## Source limitations

The main TSV is Bourdeau's ICIT-derived selection, ultimately from yajnadevam/indus-website. Every row is marked complete and has a direction: that describes a filtered source, not all excavated inscriptions. Modern proposed decipherments in upstream projects are not accepted as evidence. The M77-added and small CISI files are retained separately and NOT merged into the principal analysis; their mappings require independent checking. Photograph coverage, excavation context and chronology remain incomplete.

`sources.json` records URLs, snapshot hashes and lineage. `results/input_hashes.json` fingerprints exact analysis inputs. The source GPL-3.0 data lineage is documented in `LICENSE-DATA-GPL-3.txt`; original third-party credits remain applicable. Full scanned books are not bundled. Acquire them from the linked repositories for study; online access does not imply unrestricted image rights.

## Useful queries

```
sqlite3 results/evidence.sqlite "SELECT cisi,site,type,motif FROM objects WHERE cisi IN ('M-516','M-517');"
sqlite3 results/evidence.sqlite "SELECT * FROM substitutions WHERE left_sign='740' OR right_sign='740' LIMIT 20;"
```

Your observations from Indian languages, crafts or practices belong in the hypothesis log with a concrete prediction and a competing explanation. That makes them testable without assuming cultural continuity or a language in advance.

## Expanded run (research 03)

Run `python3 expand.py` and `python3 compare.py` for the larger 5,679-row export and all-sign comparisons. These require numpy, scipy, Pillow and fontTools. Outputs live under `expanded/`; the earlier results are preserved under `results/`. The supplied raw CSV contains upstream proposed readings, which are excluded from the analytical records.
