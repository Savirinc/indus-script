#!/usr/bin/env python3
"""Evidence-based classification for the Dravidian Database (v1.1).

Recomputes the `evidence_classification` column of pdr_04.csv from the
attestation data in dedr_entry_v11.csv, so the mechanical rule stated in the
data paper can be verified independently.

Rule (last common ancestor over the consensus subgrouping; see the paper,
Method step 4):
  - attestation in >=2 of the three macro-branches (South, Central, North)
        -> Proto-Dravidian
  - Brahui attested (alone or with Kurukh-Malto)       -> Northern Dravidian
  - Kurukh and/or Malto only (within North)            -> Kurukh-Malto Dravidian
  - Central Dravidian languages only                   -> Central Dravidian
  - South Dravidian I + (Telugu or Gondi-Kui)          -> South Total Dravidian
  - Gondi-Kui + Telugu                                 -> South Dravidian II
  - Gondi-Kui languages only                           -> Gondi-Kui
  - Telugu only                                        -> South Dravidian II
  - South Dravidian I languages only                   -> South Dravidian I

Records whose etymon has no DEDR link, or whose DEDR entry is absent from the
digitized data, keep their source_classification and carry an explicit flag in
classification_basis instead of an attestation profile.

Usage: python classify.py pdr_04.csv dedr_entry_v11.csv
Prints a per-record comparison summary; exits nonzero on any mismatch with the
shipped evidence_classification column.
"""
import csv, sys
from collections import defaultdict

SDI = {'Tamil','Malayalam','Kannada','Tulu','Kota','Toda','Kodagu','Irula',
       'Betta Kurumba','Alu Kurumba','Koraga','Belari'}
GK  = {'Gondi','Konda','Kui','Kuwi','Pengo','Manda'}
TE  = {'Telugu'}
CD  = {'Kolami','Naikri','Parji','Gadaba'}
KM  = {'Kurux','Malto'}
BR  = {'Brahui'}
UNITS = [('SDI',SDI),('Te',TE),('GK',GK),('CD',CD),('KM',KM),('Br',BR)]

def basis(langs):
    return '+'.join(tag for tag, group in UNITS if langs & group)

def lca(basis_str):
    u = set(basis_str.split('+'))
    south = bool(u & {'SDI','Te','GK'})
    macro = sum([south, 'CD' in u, bool(u & {'KM','Br'})])
    if macro >= 2:                       return 'Proto-Dravidian'
    if 'Br' in u:                        return 'Northern Dravidian'
    if 'KM' in u:                        return 'Kurukh-Malto Dravidian'
    if 'CD' in u:                        return 'Central Dravidian'
    if 'SDI' in u and (u & {'GK','Te'}): return 'South Total Dravidian'
    if 'GK' in u and 'Te' in u:          return 'South Dravidian II'
    if 'GK' in u:                        return 'Gondi-Kui'
    if 'Te' in u:                        return 'South Dravidian II'
    if 'SDI' in u:                       return 'South Dravidian I'
    return None

def main(pdr_path, entry_path):
    langs_by_num = defaultdict(set)
    with open(entry_path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['lang_str'] != 'PDr.':
                langs_by_num[row['dedr_index_id']].add(row['lang_str'])

    checked = mismatched = flagged = 0
    with open(pdr_path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            L = langs_by_num.get(row['number'], set())
            if not row['number'] or not L:
                flagged += 1
                continue
            expect = lca(basis(L))
            checked += 1
            if expect != row['evidence_classification']:
                mismatched += 1
                if mismatched <= 10:
                    print(f"MISMATCH DEDR {row['number']}: shipped="
                          f"{row['evidence_classification']!r} computed={expect!r}")
    print(f"checked: {checked} | mismatches: {mismatched} | flagged (no attestation): {flagged}")
    sys.exit(1 if mismatched else 0)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'pdr_04.csv',
         sys.argv[2] if len(sys.argv) > 2 else 'dedr_entry_v11.csv')
