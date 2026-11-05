"""Step 1: retractions only, deduplicated; field-definition flags, reason groups, dates.
Writes data/derived/records.csv (record level, not redistributed) and results/selection.json."""
import os, collections
import numpy as np, pandas as pd
from common import *

df = pd.read_csv(RAW, dtype=str, keep_default_na=False, encoding='utf-8')
n_all_rows = len(df)
nature = df['RetractionNature'].value_counts().to_dict()
r = df[df['RetractionNature'] == 'Retraction'].copy()
n_ret_rows = len(r)
r = r.drop_duplicates('Record ID')
r['ret_date'] = pd.to_datetime(r['RetractionDate'], format='%m/%d/%Y %H:%M', errors='coerce')
r['orig_date'] = pd.to_datetime(r['OriginalPaperDate'], format='%m/%d/%Y %H:%M', errors='coerce')
r['doi'] = r['OriginalPaperDOI'].str.strip().str.lower()
r.loc[~r['doi'].str.startswith('10.'), 'doi'] = ''
# duplicate DOIs (same paper entered twice): keep the earliest retraction notice
r = r.sort_values(['ret_date', 'Record ID'])
dup = (r['doi'] != '') & r.duplicated('doi', keep='first')
n_dup_doi = int(dup.sum())
r = r[~dup].copy()

r['S'] = r['Subject'].str.contains(SUBJ)
r['J'] = r['Journal'].str.contains(JOUR_INC) & ~r['Journal'].str.contains(JOUR_EXC)
r['F'] = r['Journal'].str.contains(JOUR_FOOD) & ~r['Journal'].str.contains(JOUR_EXC) & ~r['J']
r['K'] = r['Title'].str.contains(TITLE_KW)
r['primary'] = r['S'] | r['J']
r['broad'] = r['S'] | r['J'] | r['K']
r['biomed'] = r['Subject'].str.contains(r'\((?:BLS|HSC)\)')
r['glp1'] = r['Title'].str.contains(GLP1)
r['conference'] = r['ArticleType'].str.contains('Conference Abstract/Paper', regex=False)

reasons = r['Reason'].map(lambda v: set(x.lstrip('+') for x in split(v)))
for g, lst in REASON_GROUPS.items():
    s = set(lst)
    r['g_' + g] = reasons.map(lambda x: bool(x & s))
r['g_misconduct'] = r[['g_' + g for g in MISCONDUCT_GROUPS]].any(axis=1)
r['g_error_only'] = r['g_error'] & ~r['g_misconduct']
r['g_misconduct_broad'] = r['g_misconduct'] | reasons.map(lambda x: bool(x & set(MISCONDUCT_BROAD_EXTRA)))
r['g_referencing'] = reasons.map(lambda x: bool(x & set(REFERENCING)))
# reasons not mapped to any group (supplementary table): records citing each, field (primary) vs rest
mapped = set(x for v in REASON_GROUPS.values() for x in v)
allr = collections.Counter(x for s_ in reasons for x in s_)
unm = sorted((x for x in allr if x not in mapped), key=lambda x: -allr[x])
P_ = r['S'] | r['J']
unmapped = [{'reason': x, 'k_primary': int((reasons[P_].map(lambda s_, x=x: x in s_)).sum()),
             'k_rest': int((reasons[~P_].map(lambda s_, x=x: x in s_)).sum()),
             'in_broad_misconduct': x in MISCONDUCT_BROAD_EXTRA} for x in unm]
r['date_unknown'] = reasons.map(lambda x: 'Date of Article and/or Notice Unknown' in x)
r['ret_year'] = r['ret_date'].dt.year
r['pub_year'] = r['orig_date'].dt.year
ttr = (r['ret_date'] - r['orig_date']).dt.days
r['ttr_days'] = ttr.where((ttr >= 0) & ~r['date_unknown'] & r['orig_date'].notna())

keep = ['Record ID', 'doi', 'Journal', 'Publisher', 'Country', 'ArticleType', 'Title', 'ret_year', 'pub_year', 'ttr_days',
        'S', 'J', 'F', 'K', 'primary', 'broad', 'biomed', 'glp1', 'conference', 'date_unknown'] + \
       ['g_' + g for g in list(REASON_GROUPS) + ['misconduct', 'error_only', 'misconduct_broad', 'referencing']]
os.makedirs(DER, exist_ok=True)
r[keep].to_csv(os.path.join(DER, 'records.csv'), index=False)

def n(m): return int(m.sum())
sel = {
    'data': {'source': 'https://gitlab.com/crossref/retraction-watch-data', 'commit': DATA_COMMIT, 'cutoff': DATA_CUTOFF,
             'raw_sha256': sha256(RAW), 'raw_bytes': os.path.getsize(RAW)},
    'rows_all': n_all_rows, 'nature': nature, 'rows_retraction': n_ret_rows, 'dup_doi_dropped': n_dup_doi,
    'n_retractions': len(r), 'n_biomed': n(r['biomed']), 'n_with_doi': n(r['doi'] != ''),
    'n_S': n(r['S']), 'n_J': n(r['J']), 'n_F': n(r['F']), 'n_K': n(r['K']), 'n_primary': n(r['primary']), 'n_broad': n(r['broad']),
    'venn': {f'S{int(a)}J{int(b)}K{int(c)}': n(r['S'].eq(a) & r['J'].eq(b) & r['K'].eq(c))
             for a in (0, 1) for b in (0, 1) for c in (0, 1)},
    'primary_with_doi': n(r['primary'] & (r['doi'] != '')),
    'primary_conference': n(r['primary'] & r['conference']),
    'all_conference': n(r['conference']),
    'glp1_all': n(r['glp1']), 'glp1_primary': n(r['glp1'] & r['primary']), 'glp1_broad': n(r['glp1'] & r['broad']),
    'ret_year_range': [int(r['ret_year'].min()), int(r['ret_year'].max())],
    'ttr_valid_all': n(r['ttr_days'].notna()), 'ttr_valid_primary': n(r['ttr_days'].notna() & r['primary']),
    'top_journals_primary': r.loc[r['primary'], 'Journal'].value_counts().head(15).to_dict(),
    'top_journals_J': r.loc[r['J'], 'Journal'].value_counts().head(15).to_dict(),
    'top_publishers_primary': r.loc[r['primary'], 'Publisher'].value_counts().head(10).to_dict(),
    'top_publishers_all': r['Publisher'].value_counts().head(10).to_dict(),
    'glp1_titles_n_by_year': r.loc[r['glp1'], 'ret_year'].value_counts().sort_index().to_dict(),
}
sel['glp1_titles_n_by_year'] = {str(int(k)): int(v) for k, v in sel['glp1_titles_n_by_year'].items()}
dump(sel, 'selection.json')
dump({'n_distinct_reasons': len(allr), 'n_mapped_present': len([x for x in allr if x in mapped]), 'n_primary': int(P_.sum()), 'n_rest': int((~P_).sum()), 'unmapped': unmapped}, 'unmapped_reasons.json')
print('selection', len(r), sel['n_primary'], sel['n_broad'], sel['glp1_all'])
