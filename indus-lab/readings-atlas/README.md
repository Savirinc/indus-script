# Readings atlas (descriptive product, not a test, not a decipherment)

What the Indus–Brahmi atlas mapping (expanded Yajnadevam key, 714 signs; round 46) produces when applied to every inscribed object with a sign sequence in the Tejesh Raut / ICIT corpus: 4,543 records, of which 3,497 have a value for every sign.

- `ledger.csv`: one row per record, with:
  - CISI number, site, object, motif;
  - signs in reading order, the atlas values, and the reading (the author's vowel rule, round 47 `read_v`) in IAST and in Brahmi;
  - the machine Sanskrit dictionary match (DCS, CC BY 4.0) and its letter coverage;
  - the same method under a scrambled key.
- `summary.json`: dictionary coverage averages **69.0%** of letters with the atlas mapping, against **67.6%** (sd 2.1%, range 62.9–71.6%) for 20 structure-preserving scrambled keys. 4 of the 20 scrambled keys match or beat the mapping.
- `build_atlas.py`: rebuilds both, plus `atlas.html`. The owner's 1,137-page PDF (`Indus Script Decipher/readings-atlas/Indus-Readings-Atlas-Brahmi.pdf`) is printed from `atlas.html` with headless Chrome. It is not in the public repo because it embeds the unlicensed lipi Indus webfont.
- No photographs: the CISI photographs are copyrighted.

The dictionary lines are word matches, not translations. A dictionary of 134,131 headwords covers about two-thirds of any short letter string, whichever key produced it (ledger fact C19).
