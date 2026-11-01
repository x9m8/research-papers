"""Step 2: PRISMA-style flow counts from the search records, the title/abstract screen and the full-text log.
Inputs: results/records_dedup.csv, results/prescreen_counts.json, data/extraction/screening_ta_manual.csv,
data/extraction/fulltext_screening.csv, data/extraction/extraction.csv, data/extraction/replicates.csv.
Writes results/prisma.json and results/fulltext_log.csv."""
import json
import pandas as pd
from common import RES, EXT

pre = json.load(open(f'{RES}/prescreen_counts.json'))
rec = pd.read_csv(f'{RES}/records_dedup.csv').set_index('key')
ta = pd.read_csv(f'{EXT}/screening_ta_manual.csv')
ft = pd.read_csv(f'{EXT}/fulltext_screening.csv')
ex = pd.read_csv(f'{EXT}/extraction.csv')
rp = pd.read_csv(f'{EXT}/replicates.csv')

inc_ta = ta[ta.ta_include].copy()
other = ft[~ft.key.isin(inc_ta.key)]  # reports found outside the database screen (scoping brief)
inc_ta['retrieved'] = inc_ta.key.isin(ft.key)
inc_ta['is_oa'] = inc_ta.is_oa.astype(bool)
not_ret = inc_ta[~inc_ta.retrieved]
ft_assessed = ft[ft.decision.isin(['include', 'exclude'])]
reasons = ft[ft.decision == 'exclude'].reason.str.split(r' \(|;').str[0].str.strip()

def bucket(r):
    r = r.lower()
    if 'no chrome-tanned arm' in r or 'not chrome' in r or 'not described as chrome' in r or 'no chrome-free' in r or 'commercial chrome-free agent' in r: return 'no chrome-tanned control arm, or no chrome-free arm'
    if 'another publication' in r: return 'chrome values taken from another publication'
    if 'figure' in r or 'no numerical' in r or 'no physical values' in r: return 'chrome-arm values not reported numerically (figure only or absent)'
    if 'no eligible outcome' in r: return 'no eligible outcome'
    return 'other'
ftx = ft[ft.decision == 'exclude'].copy(); ftx['bucket'] = ftx.reason.map(bucket)

studies = sorted(set(ex.study_id) | set(rp.study_id))
# usable for pooling: mean and SD reported for both arms (or replicate values)
ex['has_sd'] = ex.sd_cf.notna() & ex.sd_cr.notna()
usable = {o: sorted(set(ex[(ex.outcome == o) & ex.has_sd].study_id) | (set(rp[rp.outcome == o].study_id))) for o in ['tensile', 'elongation', 'tear', 'ts']}
anydata = {o: sorted(set(ex[ex.outcome == o].study_id) | set(rp[rp.outcome == o].study_id)) for o in ['tensile', 'elongation', 'tear', 'ts']}

out = dict(
    records_identified=pre['n_records_total'], by_source=pre['by_source'], unique_after_dedup=pre['n_unique'],
    excluded_not_leather=pre['n_not_leather'], prescreen_pass=pre['n_prescreen_pass'],
    excluded_prescreen=pre['n_unique'] - pre['n_prescreen_pass'],
    ta_screened=int(len(ta)), ta_excluded=int((~ta.ta_include).sum()), ta_included=int(len(inc_ta)),
    reports_sought=int(len(inc_ta)), reports_not_retrieved=int(len(not_ret)),
    not_retrieved_closed=int((~not_ret.is_oa).sum()), not_retrieved_oa=int(not_ret.is_oa.sum()),
    reports_retrieved=int(inc_ta.retrieved.sum()), reports_other_sources=int(len(other)), other_source_keys=list(other.key), reports_duplicate=int((ft.decision == 'duplicate').sum()),
    reports_unreadable=int((ft.decision == 'unreadable').sum()),
    reports_assessed=int(len(ft_assessed)), reports_excluded=int((ft.decision == 'exclude').sum()),
    exclusion_reasons=ftx.bucket.value_counts().to_dict(),
    studies_included=len(studies), study_ids=studies,
    studies_with_any_data=({o: len(v) for o, v in anydata.items()}),
    studies_usable_for_pooling=({o: len(v) for o, v in usable.items()}),
    usable_ids=usable)
json.dump(out, open(f'{RES}/prisma.json', 'w'), indent=1)
ft.to_csv(f'{RES}/fulltext_log.csv', index=False)
print(json.dumps({k: v for k, v in out.items() if k not in ('study_ids', 'usable_ids')}, indent=1))
