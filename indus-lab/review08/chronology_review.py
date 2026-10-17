"""Audit candidate chronology without changing prior exports or source data."""
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
SOURCE = ROOT / 'raw/inscriptions.csv'
rows = list(csv.DictReader((ROOT / 'chronology/harappa_chronology_candidates.csv').open()))

def harp_candidate(row):
    # Positive provenance clue, not confirmation of a secure archaeological date.
    return bool(re.match(r'^H(?:\d{2}|20\d{2})-', row['excavation-idno']))

def signs(row):
    return re.findall(r'\d{3}', row['text'])

groups = {
    'harp_excavation_id_candidate': [r for r in rows if harp_candidate(r)],
    'other_excavation_id_scheme_unverified': [r for r in rows if not harp_candidate(r)],
}
report = {
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'harappa_rows': len(rows),
    'assigned_label_crosswalk_rows': sum(r['provisional_bin'] != 'UNASSIGNED' for r in rows),
    'notes': [
        'Original chronology export unchanged; its bins remain provisional.',
        'HARP ID detection is a provenance triage heuristic, not object dating validation.',
        'Counts are source rows and ID stems, not verified independent objects or mould families.',
        'No calendar range or sign evolution is inferred from unsupported legacy labels.',
        'Date assignments based on shape or carving cannot independently validate changes in those same features.',
    ],
    'groups': {},
    'narrow_harp_candidates': {},
}

for name, rs in groups.items():
    report['groups'][name] = {
        'rows': len(rs),
        'bins': dict(collections.Counter(r['provisional_bin'] for r in rs)),
        'target_signs': {
            s: dict(collections.Counter(r['provisional_bin'] for r in rs if s in signs(r)))
            for s in ('220', '231')
        },
    }

for period in ('3B', '3C'):
    rs = [r for r in groups['harp_excavation_id_candidate'] if r['provisional_bin'] == period]
    report['narrow_harp_candidates'][period] = {
        'rows': len(rs),
        'id_stems': len({r['id'].split('.')[0] for r in rs}),
        'types': dict(collections.Counter(r['type'] for r in rs)),
        'target_signs': {},
    }
    for sign in ('220', '231'):
        sr = [r for r in rs if sign in signs(r)]
        report['narrow_harp_candidates'][period]['target_signs'][sign] = {
            'rows': len(sr),
            'id_stems': len({r['id'].split('.')[0] for r in sr}),
            'types': dict(collections.Counter(r['type'] for r in sr)),
            'ids': [r['id'] for r in sr],
        }

target_rows = [dict(r, excavation_id_group=('harp_candidate' if harp_candidate(r) else 'other_scheme_unverified')) for r in rows if set(signs(r)) & {'220', '231'}]
with (OUT / 'chronology_220_231_review.csv').open('w') as f:
    writer = csv.DictWriter(f, fieldnames=list(target_rows[0]))
    writer.writeheader()
    writer.writerows(target_rows)
(OUT / 'chronology_review.json').write_text(json.dumps(report, indent=2))
print(json.dumps({'harappa_rows': len(rows), 'target_rows': len(target_rows), 'group_sizes': {k:len(v) for k,v in groups.items()}}, indent=2))
