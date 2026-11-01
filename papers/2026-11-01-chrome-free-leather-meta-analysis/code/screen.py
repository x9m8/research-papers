"""Step 1: merge OpenAlex + Europe PMC exports, deduplicate, apply the rule-based title/abstract pre-screen.
Writes results/records_dedup.csv and results/prescreen_counts.json. Manual screening decisions are in
data/extraction/screening_ta_manual.csv (by hand), merged in prisma.py."""
import json, re, pandas as pd
from common import RAW, RES
oa = [json.loads(l) for l in open(f'{RAW}/search_openalex.jsonl')]
ep = [json.loads(l) for l in open(f'{RAW}/search_europepmc.jsonl')]
rows = []
for r in oa: rows.append(dict(src='OpenAlex', q=r['q'], doi=(r['doi'] or '').lower(), title=r['title'] or '', year=r['year'], journal=r['journal'], abstract=r['abstract'] or '', is_oa=r['is_oa'], oa_url=r['oa_url'], authors=r['authors'], oa_id=r['id'], type=r['type']))
for r in ep: rows.append(dict(src='EuropePMC', q=r['q'], doi=(r['doi'] or '').lower(), title=r['title'] or '', year=r['year'], journal=r['journal'], abstract=re.sub('<[^>]+>', '', r['abstract'] or ''), is_oa=r['isOA'] == 'Y', oa_url='', authors=r['authors'], oa_id=r['source'] + ':' + r['id'], type=r['pubType']))
df = pd.DataFrame(rows)
n_total = len(df); n_by_src = df.groupby('src').size().to_dict()
def norm(t): return re.sub('[^a-z0-9]', '', t.lower())[:120]
df['key'] = [d if d else 't:' + norm(t) for d, t in zip(df.doi, df.title)]
# also merge DOI-less copies with the same normalised title as a DOI record
t2d = {norm(t): d for d, t in zip(df.doi, df.title) if d}
df['key'] = [k if not k.startswith('t:') or k[2:] not in t2d else t2d[k[2:]] for k in df.key]
g = df.groupby('key')
d = g.agg(title=('title', 'first'), doi=('doi', 'max'), year=('year', 'first'), journal=('journal', lambda s: max(s, key=len)),
          abstract=('abstract', lambda s: max(s, key=len)), is_oa=('is_oa', 'max'), oa_url=('oa_url', lambda s: max(s, key=len)),
          authors=('authors', 'first'), sources=('src', lambda s: ';'.join(sorted(set(s)))), queries=('q', lambda s: ';'.join(sorted(set(s))))).reset_index()
txt = (d.title + ' ' + d.abstract).str.lower()
d['leather'] = txt.str.contains(r'leather|tann(?:ing|ed|age|ery)|\bhide|\bskin', regex=True)
d['chrome'] = txt.str.contains(r'chrom|wet[- ]blue|\bbcs\b|\bcr\b|cr\(iii\)', regex=True)
d['alt'] = txt.str.contains(r'chrome[- ]free|chromium[- ]free|metal[- ]free|wet[- ]white|vegetable|glutaraldehyde|aldehyde|oxazolidine|syntan|zeolite|silica|triazine|thps|phosphonium|alumin|zirconi|titani|tannin|non[- ]chrome|ecological|eco[- ]friendly|polyphenol|chitosan|starch|collagen cross', regex=True)
d['phys'] = txt.str.contains(r'tensile|tear|shrinkage temperature|hydrothermal|elongation|physical propert|mechanical propert|strength', regex=True)
d['nohead'] = d.abstract.str.len() < 50
d['prescreen'] = d.leather & d.chrome & d.alt & (d.phys | d.nohead)
d.to_csv(f'{RES}/records_dedup.csv', index=False)
c = dict(n_records_total=n_total, by_source=n_by_src, n_unique=len(d), n_not_leather=int((~d.leather).sum()),
         n_leather=int(d.leather.sum()), n_prescreen_pass=int(d.prescreen.sum()), n_no_abstract=int(d.nohead.sum()))
json.dump(c, open(f'{RES}/prescreen_counts.json', 'w'), indent=1); print(c)
