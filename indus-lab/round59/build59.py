"""Round 59: build the frozen lexicons (no matching against any Indus text happens here). See PROTOCOL.md.
Usage: python3 -I build59.py DCS_DICTIONARY_CSV"""
import sys, csv, re, unicodedata
from pathlib import Path
P = Path(__file__).resolve().parent; LAB = P.parent; ROOT = LAB.parent
KEYWORDS = ['carnelian', 'cornelian', 'agate', 'lapis', 'beryl', 'crystal', 'gem', 'gems', 'jewel', 'jewels', 'precious stone',
            'bead', 'beads', 'pearl', 'pearls', 'coral', 'shell', 'conch', 'ivory', 'elephant', 'tusk', 'gold', 'silver', 'copper',
            'bronze', 'tin', 'metal', 'bitumen', 'wood', 'timber', 'ebony', 'rosewood', 'sandal', 'sandalwood', 'ship', 'boat',
            'cotton', 'cloth', 'garment', 'wool', 'sesame', 'barley', 'wheat', 'rice', 'grain', 'oil', 'ghee', 'butter', 'honey',
            'salt', 'peacock', 'monkey', 'dog', 'cow', 'cattle', 'bull', 'ox', 'buffalo', 'goat', 'sheep', 'ram', 'merchant',
            'trade', 'price', 'weight']
KW = re.compile(r'\b(' + '|'.join(re.escape(k) for k in KEYWORDS) + r')\b', re.I)
GREEK = {'αργυρος', 'αμφιφορευς', 'αλειφαρ', 'ελαιον', 'ελαιfον', 'ελεφας', 'ελεφαντος', 'ιππος', 'δεπας', 'χαλκος', 'χαλκον',
         'κερας', 'κριθη', 'κριθα', 'χιτων', 'κυμινον', 'χρυσος', 'κυανος', 'κυfανος', 'μελιτον', 'μελιν', 'μολυβδος', 'φασγανα',
         'φαρμακον', 'σπερμα', 'πελεκευς', 'φιαλη', 'βους', 'λινον', 'σησαμη', 'σασαμα', 'σελινον', 'οινος', 'fοινος', 'αιξ',
         'συς', 'οις', 'οfις', 'πυρος', 'σιτος', 'κοριαννον', 'ερια', 'εριον', 'φαρος'}

def write(name, rows, header):
    with (P / name).open('w', encoding='utf-8') as f:
        f.write('# ' + header + '\n')
        for r in rows: f.write('\t'.join(r) + '\n')
    print(name, len(rows))

def main(dcs):
    # Sanskrit: DCS dictionary, first sense
    com, rest = [], []
    rd = csv.reader(open(dcs, encoding='utf-8'), delimiter='\t'); next(rd)
    for r in rd:
        if len(r) < 5 or not r[1].strip(): continue
        first = r[4].split(';')[0]
        (com if KW.search(first) else rest).append((r[1], first.strip()[:80]))
    write('lex_skt_commodity.tsv', sorted(set(com)), 'Sanskrit lemma\tfirst sense (DCS dictionary, CC BY 4.0); first sense matches a keyword')
    write('pool_skt_other.tsv', sorted(set(rest)), 'Sanskrit lemma\tfirst sense; no keyword (decoy pool)')
    # Proto-Dravidian: pdr_04 reconstructions with meaning
    com, rest = [], []
    for r in csv.DictReader(open(LAB / 'external' / 'dravidian_db_v1.1' / 'pdr_04.csv', encoding='utf-8')):
        rec = r['reconstruction'].strip(); m = (r['meaning'] or '').strip()
        if not rec or rec.startswith('[') or not m: continue
        (com if KW.search(m) else rest).append((rec, m[:80]))
    write('lex_pdr_commodity.tsv', sorted(set(com)), 'Proto-Dravidian reconstruction\tmeaning (dravidian_db v1.1 pdr_04); meaning matches a keyword')
    write('pool_pdr_other.tsv', sorted(set(rest)), 'Proto-Dravidian reconstruction\tmeaning; no keyword (decoy pool)')
    # Linear B (positive control): row indices whose Greek alternatives include a commodity lemma
    rows = [l.rstrip('\n').split('\t') for l in (ROOT / 'ext' / 'neurodecipher' / 'data' / 'linear_b-greek.cog').open(encoding='utf-8')][1:]
    lb = [(str(i), g) for i, (w, g) in enumerate(rows) if set(g.split('|')) & GREEK]
    write('lb_commodity_rows.tsv', lb, 'row index in linear_b-greek.cog (0-based, header excluded)\tGreek')

if __name__ == '__main__':
    main(sys.argv[1])
