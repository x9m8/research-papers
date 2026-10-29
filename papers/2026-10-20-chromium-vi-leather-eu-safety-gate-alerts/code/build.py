"""Flatten the Safety Gate snapshot into one row per notification and classify it.

Outputs
  results/alerts.csv   one row per notification retrieved (union of searches 'chromium', 'hexavalent', 'leather')
  results/build_summary.json

Classification (text = product name + description + legal provision + risk description, English versions)
  crvi      the text names hexavalent chromium: 'chromium VI', 'chromium (VI)', 'chromium-VI', 'Cr(VI)', 'CrVI',
            'Cr VI', 'Cr6+', 'hexavalent chromium', 'chrome VI'
  leather   the text mentions leather and the leather is not described only as imitation/synthetic
  conc_*    concentrations in mg/kg extracted from sentences that mention chromium (all values, max, min)
"""
import re, json
import numpy as np, pandas as pd
from common import load, en, RES

CHR = r'(?:chro?m(?:ium|uim|iun|e)|chomium|crhomium|chromium)'
CRVI = re.compile(r'(' + CHR + r'\s*[-(]?\s*(?:VI|6)\b\s*\)?|hexavalent\s+chrom|\bCr\s*[-(]?\s*(?:VI|6\+?)\b\s*\)?|\bCrVI\b|\bCr6\+|\bCr\(VI\))', re.I)
CHROM = re.compile(CHR + r'\b|\bCr\s*\(?VI', re.I)
LEATHER = re.compile(r'leather', re.I)
# article types that are typically leather even when the alert does not say so; garments count only if 'leather' is named
ARTICLE = re.compile(r'shoe|boot|sandal|slipper|footwear|moccasin|clog|sneaker|trainer|loafer|insole|glove|mitten|handbag|wallet|purse|\bbelt|watch\s*strap', re.I)
BOILER = re.compile(r'clinical stud|sensitive subjects|Oeko.?Tex', re.I)
NONLEATHER_CATS = {'TOYS', 'COSMETICS', 'CONSTRUCTION_PRODUCTS', 'CHEMICAL_PRODUCTS', 'JEWELLERY'}
FAKE = re.compile(r'(imitation|artificial|synthetic|faux|vegan|eco|pu|pvc|simili|fake|man-made)[\s-]*leather|leatherette|leather[\s-]*(look|effect|imitation)', re.I)
NUM = r'(\d+(?:[.,]\d+)?)'
UNIT = r'\s*(?:mg\s*/\s*kg|ppm|mg\s+per\s+kg)'
VAL = re.compile(NUM + UNIT, re.I)
GKG = re.compile(r'(?<!m)' + NUM + r'\s*g\s*/\s*kg', re.I)
RANGE = re.compile(NUM + r'\s*(?:-|–|to|and)\s*' + NUM + UNIT, re.I)


CHILD = re.compile(r"child|kid|bab(y|ies)|infant|toddler|girl|boy|junior|\bteen", re.I)
TYPES = [('footwear', r'shoe|boot|sandal|slipper|footwear|moccasin|clog|sneaker|trainer|loafer|insole|flip.?flop|ballerina|\bpumps?\b'),
         ('gloves', r'glove|mitten'),
         ('garments', r'jacket|\bcoats?\b|trousers|skirt|dress|\bvest|\bhat\b|\bcap\b|garment|clothing|shorts|pants|breeches|lederhose|corset|scarf|'
                      r'blazer|\bsuits?\b|shirt|jumper|\bbra\b|bikini|lingerie|\bbody\b|jockstrap'),
         ('bags and small leather goods', r'\bbags?\b|handbag|backpack|rucksack|wallet|purse|\bcase\b|cover|pouch|\bbelts?\b|strap|bracelet|wristband|'
                      r'\bwatch\b|key.?(ring|holder)|collar|leash|\blead\b|necklace')]


def ptype(t, cat):
    t = t or ''
    for k, pat in TYPES:
        if re.search(pat, t, re.I): return k
    return 'other'


def num(s):
    return float(s.replace(',', '.'))


def sentences(t):
    return re.split(r'(?<=[.])\s+(?=[A-Z(])', t)


UNC = re.compile(r'(\(\s*)?(?:±|\+\s*/\s*-|\+-)\s*' + NUM + r'(?:\s*(?:mg\s*/\s*kg|ppm|%))?(\s*\))?', re.I)


LIST = re.compile(NUM + r'((?:\s*(?:[;,]|and|or|/)\s*(?:and\s+)?' + NUM + r')+)' + UNIT, re.I)
LIMITWORD = re.compile(r'(limit|permitted|allowed|admissible|maximum|max\.|instead of|exceed\w*|above|more than|higher than|'
                       r'greater than|less than|lower than|below|under|over|threshold|legal|restriction|requirement|<|>|≤|≥|not exceed)\W*(?:of\W*|is\W*|value\W*)*$', re.I)


OTHER = re.compile(r'\b(azo|dyes?|benzidine|aniline|amine|lead|nickel|cadmium|cobalt|mercury|arsenic|dimethyl ?fumarate|DMF|DMFu|'
                   r'PAHs?|polycyclic|phthalates?|DEHP|DBP|BBP|formaldehyde|chlorophenols?|PCP|paraffins?|SCCP|quinoline|'
                   r'DMAC|dimethylacetamide|organotin|TBT|disperse|orange|benzene|naphthalene|pentachlorophenol)\b', re.I)


TOTALCR = re.compile(r'(total|extract[ai]ble)\s+chrom\w*[^VI6]{0,15}$', re.I)


def skip(s, start):
    pre = s[max(0, start - 45):start]
    return bool(LIMITWORD.search(pre) or TOTALCR.search(pre))


def values_in(s):
    vals, spans = [], []
    for m in list(RANGE.finditer(s)) + list(LIST.finditer(s)):
        if any(a <= m.start() < b for a, b in spans): continue
        spans.append((m.start(), m.end()))
        if skip(s, m.start()): continue
        vals += [num(v) for v in re.findall(NUM, m.group(0))]
    for m in VAL.finditer(s):
        if any(a <= m.start() < b for a, b in spans): continue
        if skip(s, m.start()): continue
        vals.append(num(m.group(1)))
    return vals


def chromium_part(s):
    """Keep only the part of a sentence that belongs to chromium when other substances are also named.
    '... chromium and lead (values 4 mg/kg and 0.2 %, respectively)' -> the first value."""
    if not OTHER.search(s): return s, None
    c, o = CHROM.search(s), OTHER.search(s)
    if re.search(r'respectively', s, re.I):
        v = values_in(s)
        if v and c.start() < o.start(): return '', v[0]
        return '', None
    # split at other-substance mentions; keep the segments from a chromium mention up to the next other substance
    keep, on = [], False
    for seg in re.split(r'(?=' + OTHER.pattern + r')', s, flags=re.I):
        if CHROM.search(seg): on = True
        elif OTHER.match(seg or ''): on = False
        if on: keep.append(seg)
    return ' '.join(keep), None


def extract(text):
    """All mg/kg values attributable to chromium (VI).
    Rules: ranges and lists contribute every number; measurement uncertainties are dropped ('30.8 mg/kg ± 7.7 mg/kg');
    'mg/k' is read as mg/kg; values below 1 % by weight given as a percentage are converted (1 % = 10,000 mg/kg);
    a value preceded by limit wording ('instead of 3 mg/kg', 'less than 1 mg/kg') is skipped; in sentences that also
    name another substance only the chromium part is used. If no chromium sentence holds a value, the sentence right
    after a chromium sentence is tried ('...contain chromium VI. The measured levels were ...')."""
    text = re.sub(r'mg\s*/\s*k\b', 'mg/kg', text or '', flags=re.I)
    text = re.sub(NUM + r'\s*(?:±|\+\s*/\s*-|\+-)\s*\d+(?:[.,]\d+)?\s*(mg\s*/\s*kg)', r'\1 \2', text, flags=re.I)
    text = re.sub(r'(0[.,]\d+)\s*%(\s*by weight)?', lambda m: f'{num(m.group(1)) * 1e4:g} mg/kg', text)
    text = UNC.sub(' ', text)
    ss = sentences(text); vals = []
    for s in ss:
        if not CHROM.search(s): continue
        part, first = chromium_part(s)
        if first is not None: vals.append(first)
        vals += values_in(part)
    if not vals:
        for i, s in enumerate(ss[:-1]):
            if CHROM.search(s) and not CHROM.search(ss[i + 1]) and not OTHER.search(ss[i + 1]):
                vals += values_in(ss[i + 1])
    return [v for v in vals if 0 < v < 1e5]


d = load()
rows = []
for i, x in d['det'].items():
    p, r, m, t = x['product'], x['risk'], x['measureTaken'], x['traceability']
    name, desc = en(p.get('versions'), 'name'), en(p.get('versions'), 'description')
    legal, rdesc = en(r.get('versions'), 'legalProvision'), en(r.get('versions'), 'riskDescription')
    risktext = ' '.join(s for s in [legal, rdesc] if s)
    prodtext = ' '.join(s for s in [name, desc] if s)
    text = prodtext + ' ' + risktext
    # leather is judged from the product text and the risk sentences, leaving out generic background sentences
    # (e.g. 'clinical studies ... for leather goods' in a batch of textile notifications)
    ltext = prodtext + ' ' + ' '.join(x for x in sentences(risktext) if not BOILER.search(x))
    leather_mentions = LEATHER.findall(ltext)
    fake_mentions = FAKE.findall(ltext)
    vals = extract(risktext) or extract(text)
    rows.append(dict(
        id=int(i), ref=x['reference'], pub_date=x['publicationDate'][:10], year=int(x['publicationDate'][:4]),
        created=(x.get('creationDate') or '')[:10],
        category=p['productCategory']['name'], name=name, brand='|'.join(b['brand'] for b in p.get('brands') or []),
        risk_types='|'.join(z['name'] for z in r.get('riskType') or []),
        legal=legal, risk_desc=rdesc, description=desc,
        origin=t['countryOrigin']['name'], origin_eu=bool(t['countryOrigin'].get('euCountry')),
        notifier=x['country']['name'], notif_type=x['notificationType']['code'],
        measures='|'.join(sorted(set(z['measureType']['name'] for z in m.get('measures') or []))),
        measure_cats='|'.join(sorted(set(z['measureCategory']['name'] for z in m.get('measures') or []))),
        sold_online=t['isSoldOnline']['name'],
        search_tags='+'.join(sorted(d['ids'][i])),
        crvi=bool(CRVI.search(text)),
        chromium_any=bool(CHROM.search(text)),
        leather=len(leather_mentions) > len(fake_mentions),
        leather_any=bool(leather_mentions),
        article=bool(ARTICLE.search(name or desc or '')) and p['productCategory']['name'] not in NONLEATHER_CATS,
        unit_gkg=bool(GKG.search(risktext)),
        n_vals=len(vals), conc_max=max(vals) if vals else np.nan, conc_min=min(vals) if vals else np.nan,
        conc_all=';'.join(f'{v:g}' for v in vals),
        ptype=ptype(prodtext, p['productCategory']['name']),
        child=bool(CHILD.search(prodtext)),
        comp_insole=bool(re.search(r'insole|footbed|sock\b|sock lining', risktext, re.I)),
        comp_lining=bool(re.search(r'lining', risktext, re.I)),
        comp_upper=bool(re.search(r'\bupper', risktext, re.I))))
df = pd.DataFrame(rows).sort_values('pub_date').reset_index(drop=True)
df.to_csv(f'{RES}/alerts.csv', index=False)
# Scope: Cr(VI) notifications for leather or leather-type articles (shoes, gloves, bags, ...), excluding cement,
# cosmetics, toys, jewellery and chemical products, which fall under other Cr(VI) limits.
# jewellery is in scope only when the product text names real leather (e.g. a leather necklace)
df['scope'] = df.crvi & (df.leather | (df.article & ~df.leather_any)) & \
    (~df.category.isin(NONLEATHER_CATS) | ((df.category == 'JEWELLERY') & df.leather))
df.to_csv(f'{RES}/alerts.csv', index=False)
core = df[df.scope]
summ = dict(retrieved=d['retrieved'], n_notifications=len(df), n_crvi=int(df.crvi.sum()), n_leather=int(df.leather.sum()),
            n_scope=len(core), n_scope_leather_word=int((core.leather).sum()), n_scope_with_conc=int(core.conc_max.notna().sum()),
            n_chromium_not_crvi=int((df.chromium_any & ~df.crvi).sum()),
            first=df.pub_date.min(), last=df.pub_date.max(),
            totals_by_year={int(k): v for k, v in d['totals'].items()})
json.dump(summ, open(f'{RES}/build_summary.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in summ.items() if k != 'totals_by_year'}, indent=1))
