# Conjectures about the Indus script, stated so that they can be wrong

*Maintained from 18 October 2026. Each entry gives the conjecture, what it explains, the evidence for and against as of today, and the observation that would refute it. A conjecture that cannot be refuted by any observation is listed as such. Following Popper and Deutsch: an explanation earns its place by being hard to vary while still accounting for the evidence, and by saying what would kill it.*

Status words: **ESTABLISHED** (survived pre-registered controls), **OPEN** (live, testable, untested or inconclusive), **REFUTED** (failed a pre-registered test here), **UNTESTABLE NOW** (no instrument or data can decide it today), **CLOSED** (the data that could decide it has been examined and is empty).

---

## A. The nature of the system

### A1. The Indus signs are a writing system that encodes language
- **Explains:** stable sign order, fixed endings, repeated sequences across sites, variable texts under a constant emblem.
- **For:** bigram structure transfers between Harappa and Mohenjo-daro (rounds 27, 29); endings fixed per text (round 34 audit); Gulf-made seals deviate from the native order, as foreign use would (rounds 30–31).
- **Against:** no text longer than 17 signs; no bilingual; texts are mostly unique; Farmer, Sproat and Witzel's non-linguistic reading accounts for the brevity.
- **Refuted by:** a demonstration that a non-linguistic generative model (emblem combinatorics) reproduces the conditional sign-order statistics as well as the bigram model does. Round 28 tried and was inconclusive. Round 52b shows that entropy, inventory and Heaps statistics cannot settle this either way: real non-phonetic administrative systems (Uruk III proto-cuneiform H2/H1 0.51, proto-Elamite 0.47) match phonetic scripts (Ur III Sumerian 0.48, Egyptian 0.56) at matched size, so Rao et al.'s conditional-entropy argument does not discriminate. Only a generative comparison that beats the proto-cuneiform control (round 56) can move this.
- **Status:** OPEN, leaning linguistic on sign-order transfer and foreign-seal evidence, not on entropy. Nothing here assumes it.

### A2. The texts on seals are names and titles of persons or offices
- **Explains:** 892 distinct texts among 1,005 unicorn-seal inscriptions; length 2–8 signs; fixed terminal signs behaving like suffixes; the pattern of every deciphered seal tradition.
- **For:** the frequency profile (median sign appears twice); Gulf seals carry non-Harappan sequences in the same slots, as foreign names would.
- **Against:** none decisive; some texts on tablets look like formulae rather than names.
- **Refuted by:** a bilingual showing a seal text to be a commodity list or a dedication.
- **Status:** OPEN, best-supported account of content.

### A3. The script is logosyllabic (word signs plus syllable signs), like early cuneiform or Linear B
- **Explains:** 400–700 sign types, too many for an alphabet or pure syllabary, too few for a logography.
- **For:** inventory size; compound signs built from basic ones; numeral strokes.
- **Against:** none decisive.
- **Refuted by:** sign-frequency and order statistics that match an alphabetic, syllabic or purely logographic system under a pre-registered comparison with real corpora at matched size and text length. Round 52 ran this with Greek, Hebrew, Cherokee, Ur III Sumerian, Egyptian, oracle-bone Chinese and the Shijing: the alphabet and syllabary alternatives are excluded (control passed; Indus three to ten times further from them than from any large-inventory system), but the logosyllabic-versus-logographic distinction was not separable with one or two corpora per class (METHOD-FAIL on that half). A decisive version needs at least three excavated corpora per large-inventory class.
- **Status:** OPEN, narrowed: a large-inventory system; on every structural statistic the Indus corpus is nearest the Shang oracle-bone inscriptions by a factor of four to five over any other corpus, stable under every leave-one-out (round 52b), which fits short formulaic records of names and titles (A2) more than it decides A3. The "monosyllabic" variant (each sign one one-syllable word, as in Old Chinese) is not excluded by rounds 52–52b and could not be tested by PMI segmentation at this corpus size (round 53, METHOD-FAIL); round 54 tried combinatorial freedom as the signature of a syllabic core and found it does not work on Akkadian controls either (METHOD-FAIL). After rounds 52–54 no generic sign statistic distinguishes logosyllabic from one-sign-per-word writing at this corpus size; 53b (Dirichlet-process lexicon induction) failed its control by 0.001 on two corpora; descriptively Indus segments like the one-sign-per-word Shijing, but the Shijing is not separated from Akkadian on that statistic. The structural track cannot decide A3's syllabic component. One new constraint: only 3.5% of Indus texts repeat a sign, against 14% for Sumerian and 28% for Egyptian; any key must reproduce this.

## B. The language

### B1. The Harappan language was Dravidian
- **Explains:** the Dravidian lean of Rigvedic substrate words (rounds 39–40); Brahui in Baluchistan; the fish/star rebus fitting Dravidian; Parpola's Meluhha = mēl-akam; retroflexes in Indo-Aryan.
- **For:** rounds 39–40 (substrate leans Proto-Dravidian over Munda, not a dictionary-size artefact).
- **Against:** every Dravidian key fails its shuffle test (Fairservis, round 49) or is matched by Finnish (rounds 41–45); the rebus method fails its Chinese control (round 36); Meluhhan loanwords show no Dravidian signal beyond one sesame word (round 51); Brahui's presence in Baluchistan is medieval by one scholarly account.
- **Refuted by:** anchored sign values that read as something else; or substrate words that attribute elsewhere once the sample grows.
- **Status:** OPEN. The best-supported family hypothesis, by a small margin, on evidence that is about the substrate rather than the script.

### B2. The Harappan language was Indo-Aryan or Sanskrit
- **Explains:** nothing that B1 does not; it is proposed on the readings of keys (Rao, Kak, Yajnadevam, Bonta) and on Brahmi look-alikes.
- **For:** none that survives a control. The shape resemblance to Brahmi is untestable (round 48).
- **Against:** Yajnadevam's and Rao's keys fail their shuffle tests and are out-fitted by Finnish (rounds 47, 49); the Rigveda knows no cities, seals, writing or brick and is horse-centred where the Indus has no horse; ancient DNA shows no steppe ancestry in Indus-period individuals, with steppe ancestry arriving after 2000 BCE; Indo-Aryan names first appear in cuneiform around 1400 BCE in Syria, never in the Gulf or Meluhha texts; the mleccha etymology, if accepted, records that Vedic speakers regarded the Meluhhans as foreign.
- **Refuted by:** already refuted in every testable form. Would be revived by a Harappan-period Indo-Aryan name or word in cuneiform, or by anchored sign values reading as Indo-Aryan.
- **Status:** REFUTED in its published forms; the family hypothesis itself survives only as "not yet tested with anchors".

### B3. The Harappan language was Munda / Para-Munda (Witzel) or an isolate
- **Explains:** prefixing substrate words in the Rigveda; the failure of both Dravidian and Indo-Aryan keys.
- **For:** Kuiper's prefixed words; Witzel's analysis.
- **Against:** rounds 39–40 attribute the glossed substrate words to Dravidian over Munda; Munda matched nothing in round 51.
- **Refuted by:** the same observations as B1, in reverse.
- **Status:** OPEN, weaker than B1 on current evidence.

### B4. The seal language differs from the spoken substrate language
- **Explains:** why substrate evidence (B1) and seal evidence can disagree: an administrative or elite language on seals, another in the villages.
- **Refuted by:** anchored sign values matching the substrate family.
- **Status:** UNTESTABLE NOW. Worth stating because it blocks any inference from B1 to the script.

## C. Sign values

### C1. Any specific published key (Yajnadevam, Rao, Fairservis, Parpola, Kak, Mahadevan, Bonta, Bhaty)
- **Refuted by:** reading no better than one's own shuffles; being out-fitted by an impossible language.
- **Status:** REFUTED for Yajnadevam, Rao and Fairservis, and for Bhaty's place-name variant of Yajnadevam's key (round 57: place names no commoner than under shuffles; Linear B control passed); NOT TESTABLE for Parpola, Kak and Mahadevan on this corpus; Bonta UNTESTED (copy not obtainable). Round 58: any *bijective* one-syllable-per-sign Sanskrit or Old Tamil key is excluded in 10 of 14 conditions by the repetition rate alone (ledger X7); keys with homophones, such as Yajnadevam's, are outside that exclusion.

### C2. Some sign values can be recovered from internal statistics alone
- **Refuted by:** round 32: Linear B at Indus density collapses, wrong keys outscore the true key.
- **Status:** REFUTED at current corpus size. Reopened only by a corpus several times larger or by ~40 anchors.

### C3. The jar sign (740) is a grammatical suffix
- **Explains:** its position (text-final in 28% of texts), its fixedness per name, its absence from Gulf-made seals' native slots.
- **Against:** none.
- **Refuted by:** a bilingual showing it to be a word.
- **Status:** OPEN, function well supported, value unknown. Every proposed sound for it (Mahadevan -anru, Yajnadevam -an, Kak sa) is untested or failed.

### C4. The fish sign (220) means "star" by Dravidian rebus (mīn)
- **Refuted by:** round 36: the rebus method ranks the true Chinese key 14th of 16 on real Chinese; round 34: the "6 + fish = Pleiades" count does not hold in the CISI transcriptions. 
- **Status:** REFUTED as an argument; the reading itself is unfalsifiable without anchors and is therefore not evidence.

## D. External connections

### D1. Meluhha in cuneiform texts is the Indus region
- **For:** goods, dates, find-spots of Indus seals and beads; mainstream consensus since the 1930s.
- **Refuted by:** a Meluhhan product list naming things the Indus could not supply, or Indus material absent from the right Mesopotamian horizons. Neither exists.
- **Status:** ESTABLISHED by archaeology, not by this project.

### D2. Sanskrit mleccha derives from Meluhha (Parpola 1975, Witzel 1999)
- **Explains:** Pali milakkha closer to Meluhha; the toponym-to-"outsider" pattern (Franks → farangi).
- **Against:** the -ḫḫ- to -cch- change is unexplained; first attestation ~800 BCE; Mayrhofer marks it unprovable; rival etymologies exist.
- **Refuted by:** a Middle Indo-Aryan attestation showing the word's form before contact could have happened, or a regular Indo-Aryan derivation.
- **Status:** OPEN. If true, it records that Vedic speakers saw the Meluhhans as foreigners, which counts against B2.

### D3. Gulf-made round seals spell Dilmunite names with borrowed Indus signs
- **For:** rounds 30–31: foreign sign order; the "twins" sign concentrated there.
- **Against:** round 35 could not match them to the 27 attested names; fake names match as well.
- **Refuted by:** a Gulf seal whose signs cannot be a name under any consistent mapping once more names are known.
- **Status:** OPEN; the most promising anchor route; blocked by sample size.

### D4. Brahmi descends from the Indus script
- **For:** shape resemblances (Hunter 1934, Rao, Kak, Yajnadevam); some Indus-like graffiti on later potsherds.
- **Against:** 1,500 unattested years; mainstream Aramaic derivation; round 48 shows the shape argument cannot be tested with fonts in either direction.
- **Refuted by:** nothing available. Would be supported by intermediate inscriptions with datable contexts.
- **Status:** UNTESTABLE NOW with typographic data; needs epigraphic tracings. Even if true, it would not fix sound values or language (script ≠ language; 1,500 years of sound drift).

### D5. The Indus–Mesopotamia contact left a bilingual or near-bilingual
- **Status:** CLOSED on the published record (round 50: no Indus-sign impression on any inscribed tablet; round 51: no Meluhhan loanword list exists). Reopened only by new tablets or unpublished Lagash archives.

## E. Iconography

### E1. The unicorn is the emblem of a dominant group or office, not a real animal
- **For:** two-horned animals are drawn with both horns elsewhere; no single-horned bovid in any faunal assemblage; the fixed iconographic package; 892 different texts under it.
- **Refuted by:** a one-horned bovid skeleton from a Harappan site.
- **Status:** OPEN, strongly supported.

### E2. The seated horned figure (M-304) is a proto-Shiva
- **For:** posture, horns, animals, later Pashupati iconography.
- **Against:** a thousand Shiva epithets guarantee matches to any seated horned figure; equally matched by Mesopotamian and Celtic horned gods; rival readings (buffalo-headed man, buffalo demon).
- **Refuted by:** an epithet-matching test against a decoy set of unrelated horned figures in which M-304 does not beat the decoys. Not yet run.
- **Status:** OPEN, and neutral between language hypotheses even if true.

---

## What would move the whole picture

Ranked by how much it would unlock: (1) a bilingual; (2) a long text, which Ganweriwala, unexcavated, is the likeliest place to hold; (3) twenty or more Meluhhan personal names in Ur III ration lists; (4) an Indus-sign seal impression on an inscribed tablet in unpublished material; (5) more ancient DNA, which settles people, not script. Until one of these appears, every reading of the seals is a conjecture that no observation can yet refute, and that is the definition of a claim not ready to be believed.
