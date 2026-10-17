# Working backwards toward ancestral Dravidian

11 October 2026. This checkpoint organizes existing comparative evidence; it does not reconstruct a whole language or decode Meluhhan. Modern Tamil is one descendant, not a reversible recording of the ancestral language. Proto-Dravidian means a reconstructed common ancestor, not the first human language or a fully recovered first historical version.

## Executed work

The program processed the frozen DravLex snapshot used in our earlier experiments. Of 2,127 forms, 1,986 satisfy the supplied nonloan flag, segmentation and cognacy filters. They cover 100 concepts and 20 languages, yielding 732 exact concept/cognacy-label groups, of which 253 contain more than one language. These are imported scholarly cognacy judgements, not 253 newly discovered roots. Forms and metadata are retained in comparative_ledger.json; no automatic proto-form is asserted.

Initial sound correspondences are counted across paired languages within those groups. Synonyms do not multiply identical concept-level correspondences. The code makes no claim to establish sound-change direction, conditioning, chronology or complete word alignment.

## Concrete example: tooth

The dataset groups tooth forms from 18 languages together. Selected recorded forms:

| Language | Dataset transcription |
|---|---|
| Tamil | pallə |
| Malayalam | pallə |
| Kannada | hallu |
| Telugu | pannu |
| Gondi | pal |
| Kurukh | pall |

These are the dataset's transcriptions, not normalized dictionary headwords. Its Brahui tooth entries are flagged as loans and excluded, illustrating why geographic location alone is not evidence of inherited vocabulary.

Excluding tooth, Tamil initial p corresponds to Kannada h in eight concepts: fly, green, louse, many, name, new, smoke and woman. Foot supplies a p:p exception under the dataset's classifications. The tooth correspondence p:h agrees with the recurring pattern. This is a descriptive, retrospectively selected check, not a blinded validation or a newly discovered sound law.

Published linguistic work independently gives Proto-Dravidian *pal 'tooth'. The asterisk means reconstructed, not directly attested. Masato Kobayashi, Historical Phonology of Old Indo-Aryan Consonants (2004), printed p163/PDF173, contrasts this short-vowel root with *pāl 'milk'. Vowel length must be preserved. Source: https://gengo.l.u-tokyo.ac.jp/masatok/hpiac_2004.pdf .

## The proposed Meluhha bridge

Mukhopadhyay (2021) connects the inherited tooth root to proposed elephant/ivory forms and words recorded in Near Eastern languages. The robust comparative tooth family and the proposed trade-word borrowing route are separate evidential steps. A cuneiform word is attested in its recording language; its proposed donor language is an inference. No Meluhhan transcription or Indus sign value is supplied by this etymology alone. Source: https://doi.org/10.1057/s41599-021-00868-w .

The additional source note records the cited attestations and the unresolved transformations. Earlier sources cited by that article must be checked at tablet/edition level before an exact donor reconstruction can be treated as a constraint.

## Mechanism to extend this work

1. Import published ancestral reconstructions with source, subgroup level, alternative forms and uncertainty; do not generate proto-forms by majority vote.
2. Link them to attested Old Tamil, Old Kannada and other historical forms, then to modern cognate sets. Modern forms alone cannot date sound changes or undo all mergers.
3. Model recurrent, conditioned correspondences and morphology; test predictions on excluded cognate sets. Retain alternative ancestral forms when evidence cannot distinguish them.
4. Audit externally recorded possible loanwords and names, including earliest attestation, recording language, meaning, chronology and competing etymologies.
5. Only then evaluate explicit sign-to-sound proposals, consistently across Indus inscriptions and independent archaeological constraints. A word denoting an Indus trade commodity does not by itself identify the language or a corresponding written sign.

Current status: comparative data indexed; one published reconstruction grounded; Meluhhan connection remains a hypothesis. No proto-language sentence, Meluhhan word or Indus translation has been generated as fact.

## Reproduce

Run `python indus-lab/round21/build_comparative.py` from the extracted archive root. Standard library only. Input hash and counts appear in summary.json. The original DravLex forms, source bibliography, provenance and CC BY 4.0 licence accompany the code.
