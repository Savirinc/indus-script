"""Round 58: download raw sources (outside the repo). Usage: python3 -I fetch58.py RAWDIR
DCS CoNLL-U (Ṛgveda, Rāmāyaṇa) and dictionary, CC BY 4.0; Puṟanāṉūṟu wikitext from ta.wikisource.org."""
import sys, json, time, urllib.request, urllib.parse
from pathlib import Path
RAW = Path(sys.argv[1]); RAW.mkdir(parents=True, exist_ok=True)
GH = 'https://api.github.com/repos/OliverHellwig/sanskrit'
RAWGH = 'https://raw.githubusercontent.com/OliverHellwig/sanskrit/master/'
def get(url, tries=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'indus-script-round58 (research)'})
            return urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(5 * 2 ** min(i, 4))   # back off (Wikisource answers 429 to fast clients)

# DCS: list text directories through the git tree of dcs/data/conllu/files (no 1,000-entry cap)
parent = json.loads(get(GH + '/contents/dcs/data/conllu'))
fsha = [e['sha'] for e in parent if e['name'] == 'files'][0]
dirs = json.loads(get(GH + f'/git/trees/{fsha}'))['tree']
for text in ['Ṛgveda', 'Rāmāyaṇa']:
    dsha = [e['sha'] for e in dirs if e['path'] == text][0]
    tree = json.loads(get(GH + f'/git/trees/{dsha}'))
    assert not tree.get('truncated')
    names = sorted(e['path'] for e in tree['tree'] if e['path'].endswith('.conllu'))
    out = RAW / text; out.mkdir(exist_ok=True)
    for n in names:
        f = out / n
        if not f.exists():
            f.write_bytes(get(RAWGH + urllib.parse.quote(f'dcs/data/conllu/files/{text}/{n}')))
    print(text, len(names), 'files')
(RAW / 'dictionary.csv').write_bytes(get(RAWGH + 'dcs/data/conllu/lookup/dictionary.csv'))

# Puṟanāṉūṟu: all subpages of the main page on Tamil Wikisource, as wikitext
API = 'https://ta.wikisource.org/w/api.php?'
def wiki(params): return json.loads(get(API + urllib.parse.urlencode(dict(params, format='json'))))
main = 'புறநானூறு'
pages = []; cont = {}
while True:
    d = wiki(dict(action='query', list='allpages', apprefix=main + '/', apnamespace=0, aplimit=500, **cont))
    pages += [p['title'] for p in d['query']['allpages']]
    if 'continue' not in d: break
    cont = {'apcontinue': d['continue']['apcontinue']}
out = RAW / 'puram'; out.mkdir(exist_ok=True)
for t in pages:
    f = out / (t.replace('/', '__') + '.wiki')
    if f.exists(): continue
    time.sleep(1.5)
    d = wiki(dict(action='query', prop='revisions', rvprop='content|ids', rvslots='main', titles=t))
    p = list(d['query']['pages'].values())[0]
    f.write_text(p['revisions'][0]['slots']['main']['*'], encoding='utf-8')
print('puram subpages', len(pages)); print('\n'.join(pages))
