# CISI volume 2 pilot: verified extraction, unresolved readings

10 October 2026. Prepared for Arham Partap Jain.

## Completed deliverable

The first pilot is a reproducible, image-linked set of five catalogue objects and ten faces: M-1543 through M-1547, CISI2 printed page226 / PDF page261. An offline HTML review document displays every crop, its native dimensions, the intact parent page and the two visual assessments. The machine-readable records and extraction code are in the companion bundle.

This is a targeted difficult page selected around the copper-tablet problem, not a representative sample of CISI2. It tests whether our process preserves evidence and abstains when necessary; it does not estimate recognition accuracy over the whole volume.

| Result | Count |
|---|---:|
| Catalogue objects recorded | 5 |
| A/B face records and crops | 10 |
| Exact source-pixel crop checks passed | 10 |
| Objects matched to current CSV by catalogue ID | 1 |
| Catalogue objects without a matching ID in the CSV | 4 |
| Faces where both AI reviewers abstained from full transcription | 10 |
| Newly deciphered signs or certified complete sequences | 0 |

## What the pilot establishes

The embedded JPEG was extracted from the source PDF without resampling. Each PNG crop exactly preserves its corresponding decoded source pixels. Cropping rectangles, original-page coordinates, hashes and printed/PDF page references are recorded. Both face labels are present for every object; no crop includes another object. An independent code-and-image check confirmed these properties.

Two AI reviewers inspected the native page separately without supplied sign IDs, readings or proposed meanings. Their descriptions preserve local visible features while declining to supply full sequences. Agreement between AI reviewers is not external archaeological validation, and their errors may be correlated. Their comments remain separately attributable rather than becoming a single invented transcription.

The dataset distinguishes four layers: catalogue identity; photographic observation; imported transcription assertions; and interpretation. Only the first three have entries, and imported assertions are explicitly unverified. The transcription field stays null where the photograph does not support a complete reading; null does not mean blank, zero signs or absent writing.

## A concrete coverage finding

Only M-1547 matches the current CSV. M-1543, M-1544, M-1545 and M-1546 do not match, including an independent relaxed search for M-prefixed aliases. Similar H-prefixed numbers refer to a different catalogue namespace and must not be merged.

This does NOT establish four newly discovered inscriptions, nor prove that the live ICIT database lacks them. The current CSV may omit indistinct/non-transcribed material, or another identifier may exist in an unexamined source. It demonstrates why a complete photograph catalogue and a text-analysis CSV should not be treated as interchangeable.

The two M-1547 CSV records assert `+407-321-407-845-033-705-235+` and `+753+`. They are retained exactly as imported. Decimal record suffixes are NOT automatically assigned to the printed A/B faces. Neither imported string was promoted into a verified photographic reading.

## Scan-quality inventory

We indexed the embedded-image dimensions across all486 pages of this volume2 scan. The largest image on every page gives approximately100 horizontal pixels per inch when related to the PDF page width. This is raster metadata, not a reading or object-level digitisation of all486 pages. The pilot page itself is805×1132 pixels.

Enlargement does not recover missing observations. No generative restoration, sharpening, rotation, mirroring or contrast manipulation was used. The original page is preserved so crops and captions can be checked. The downloadable bundle includes only this selected page and its crops, not the complete book.

## Next evidence queue

First: obtain better photographs or independent earlier plates for M-1547 A/B and verify its catalogue/group assignment. It has explicit imported strings and matters to the proposed alternate-reverse relationship, making it more informative than an arbitrary new image.

Next: resolve the four unmatched catalogue IDs and find better views of their markings. Record whether each is genuinely inscribed, indistinct or outside the transcription corpus; do not equate an unreadable scan with a blank ancient surface.

For expansion, add contrasting pages with clearer inscriptions and hold back a reviewed subset to evaluate segmentation and recognition. This pilot has no positive legibility cases, so it cannot validate an automatic sign recogniser. Photographic transcription should remain blind to Tamil or other proposed readings. Language hypotheses can be tested after the observation layer is fixed.

## Reproduction and files

Requirements: Python3, PyMuPDF (`fitz`) and Pillow. From the unpacked bundle:

```bash
python3 indus-lab/round18/build_pilot.py --pdf /path/to/CorpusVol2.pdf --corpus /path/to/inscriptions.csv
python3 indus-lab/round18/index_volume.py --pdf /path/to/CorpusVol2.pdf
python3 indus-lab/round18/build_review.py
```

The extraction script pins the source PDF hash. Reviewer files are included as human-readable records of separate AI assessments; the build does not regenerate them. A changed source scan requires new coordinates and review.

- `objects.json`, `faces.json`, `reviewed-faces.json`: object/face relationships, crops and uncertainty.
- `source.json`, `page-image-index.json`: source provenance and raster inventory.
- `imported-assertions.json`, `coverage.json`: existing CSV assertions and catalogue matching.
- `reviewer-a.json`, `reviewer-b.json`: separate visual assessments.
- `validation.json`, `independent-integrity-review.md`: checks and their limits.
- `acquisition-queue.json`: prioritized missing evidence.
- `images/`: original embedded page and ten lossless crops.
- `review.html`: portable review document with embedded images.

Source: Shah and Parpola (eds.), *Corpus of Indus Seals and Inscriptions 2: Collections in Pakistan* (1991), printed226. Scan: https://archive.org/download/corpus-vol-2_202409/CorpusVol2.pdf . PDF SHA256:727132579a485ee626e48a64c663148a85fbc0811fb523818fd615231f8a327d. Public access does not establish an open licence for all source imagery. No claim of a decipherment or a completed whole-volume transcription is made.
