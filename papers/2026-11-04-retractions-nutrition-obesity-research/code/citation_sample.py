"""Step 3a: DOIs for the post-retraction citation analysis -> data/derived/citation_dois.json (record level, not redistributed).
Field set: every primary-definition retraction with a DOI retracted 2012-2023. Comparison set: a random sample of other
biomedical retractions (BLS/HSC subject, not in the field) with a DOI, stratified to the same retraction years, two per field record."""
import os, json
import numpy as np, pandas as pd
from common import *

r = pd.read_csv(os.path.join(DER, 'records.csv'), dtype={'Record ID': str, 'doi': str}, keep_default_na=False,
                na_values={'ret_year': [''], 'pub_year': [''], 'ttr_days': ['']})
for c in ['primary', 'biomed']:
    r[c] = r[c].astype(str).eq('True')
rng = np.random.default_rng(SEED)
ok = (r['doi'] != '') & r['ret_year'].between(2012, 2023)
field = r[ok & r['primary']]
pool = r[ok & r['biomed'] & ~r['primary']]
comp = []
for y, g in field.groupby('ret_year'):
    cand = pool[pool['ret_year'] == y]
    k = min(len(cand), 2 * len(g))
    comp.append(cand.iloc[rng.choice(len(cand), k, replace=False)])
comp = pd.concat(comp)
out = [{'doi': d, 'group': 'field', 'ret_year': int(y), 'pub_year': (None if pd.isna(p) else int(p))} for d, y, p in field[['doi', 'ret_year', 'pub_year']].itertuples(index=False)]
out += [{'doi': d, 'group': 'comparison', 'ret_year': int(y), 'pub_year': (None if pd.isna(p) else int(p))} for d, y, p in comp[['doi', 'ret_year', 'pub_year']].itertuples(index=False)]
os.makedirs(DER, exist_ok=True)
json.dump(out, open(os.path.join(DER, 'citation_dois.json'), 'w'))
print('citation sample', len(field), len(comp))
