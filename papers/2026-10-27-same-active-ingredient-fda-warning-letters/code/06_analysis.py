"""Descriptive analysis of the final (adjudicated) codes.
Outputs: results/flow.json, results/prevalence.csv, results/prevalence_by_seller.csv, results/timeline.json,
results/waves.csv, results/recalls.json, results/summary.json, results/open_dataset.csv
"""
import json, re
import numpy as np, pandas as pd
from statsmodels.stats.proportion import proportion_confint
from common import RES, RAW, LETTERS, CODES, CODE_LABEL, EVENTS

idx = pd.read_csv(f'{RES}/corpus_index.csv', parse_dates=['issued_date', 'posted_date'])
fc = pd.read_csv(f'{RES}/final_codes.csv')
df = idx.merge(fc, on='slug')
man = json.load(open(f'{RES}/snapshot_manifest.json'))

# ---------- flow ----------
flow = dict(records_by_term=man['query_counts'], records_total=int(sum(man['query_counts'].values())),
            unique_letter_urls=len(df), duplicate_postings=int(df.text_sha256.duplicated().sum()),
            full_text_retrieved=int((df.http_status == 200).sum()),
            excluded_brand_holder=int((df.exclusion == 'X1_brand_holder').sum()),
            excluded_incidental=int((df.exclusion == 'X2_incidental').sum()),
            excluded_slugs={s: e for s, e in zip(df.slug, df.exclusion) if isinstance(e, str) and e},
            included=int(df.eligible.sum()))
json.dump(flow, open(f'{RES}/flow.json', 'w'), indent=1)
inc = df[df.eligible == 1].copy()
N = len(inc)

# seller groups for reporting
GROUP = {'telehealth': 'Telehealth platform', 'clinic_medspa': 'Clinic / med spa', 'online_pharmacy': 'Online pharmacy / marketplace',
         'research_chem': 'Research-chemical seller', '503A': 'Compounder (503A/503B)', '503B': 'Compounder (503A/503B)',
         'api_supplier': 'API supplier / other manufacturer', 'other': 'API supplier / other manufacturer'}
ORDER = ['Telehealth platform', 'Clinic / med spa', 'Online pharmacy / marketplace', 'Research-chemical seller',
         'Compounder (503A/503B)', 'API supplier / other manufacturer']
inc['group'] = inc.seller_type.map(GROUP)

def wilson(k, n):
    lo, hi = proportion_confint(k, n, method='wilson'); return float(lo), float(hi)

# ---------- prevalence ----------
prev = []
for c in CODES:
    k = int(inc[c].sum()); lo, hi = wilson(k, N)
    prev.append(dict(code=c, label=CODE_LABEL[c], n=k, N=N, pct=k / N, lo=lo, hi=hi))
prev = pd.DataFrame(prev); prev.to_csv(f'{RES}/prevalence.csv', index=False)
bys = []
for g in ORDER:
    sub = inc[inc.group == g]
    for c in CODES:
        k = int(sub[c].sum()); lo, hi = wilson(k, len(sub))
        bys.append(dict(group=g, code=c, n=k, N=len(sub), pct=k / len(sub), lo=lo, hi=hi))
bys = pd.DataFrame(bys); bys.to_csv(f'{RES}/prevalence_by_seller.csv', index=False)
seller_counts = inc.seller_type.value_counts().to_dict()
group_counts = inc.group.value_counts().reindex(ORDER).to_dict()

# products named (regex on letter text; descriptive)
PROD = {'semaglutide': r'semaglutide|\bsema\b|GLP-1[ -]?S\b|GLP-1 SEM|GLP-1 SM', 'tirzepatide': r'tirzepatide|\btirz\b|GLP-2[ -]?T|GLP-2 TRZ|GLP-2 TZ',
        'retatrutide': r'retatrutide|\breta\b|GLP-3', 'liraglutide': r'liraglutide', 'cagrilintide': r'cagrilintide|\bcagri',
        'mazdutide_or_survodutide': r'mazdutide|survodutide'}
prod = {}
for k, rx in PROD.items():
    prod[k] = int(sum(bool(re.search(rx, open(f'{LETTERS}/{s}.txt').read(), re.I)) for s in inc.slug))

# ---------- timeline ----------
inc['month'] = inc.issued_date.dt.to_period('M').astype(str)
inc['quarter'] = inc.issued_date.dt.to_period('Q').astype(str)
by_date = inc.groupby('issued').size().sort_values(ascending=False)
batches = {d: int(n) for d, n in by_date.items() if n >= 3}
batch_n = int(sum(batches.values()))
by_year = inc.issued_date.dt.year.value_counts().sort_index()
lag = (inc.posted_date - inc.issued_date).dt.days
cut = pd.Timestamp('2025-05-22')
timeline = dict(by_year={int(k): int(v) for k, v in by_year.items()}, by_quarter=inc.quarter.value_counts().sort_index().to_dict(),
                batch_dates=batches, batch_letters=batch_n, batch_share=batch_n / N,
                top3_dates={d: int(n) for d, n in by_date.head(3).items()}, top3_letters=int(by_date.head(3).sum()), top3_share=float(by_date.head(3).sum() / N),
                n_issue_dates=int(len(by_date)), n_single_letter_dates=int((by_date == 1).sum()),
                first_issue=str(inc.issued_date.min().date()), last_issue=str(inc.issued_date.max().date()),
                before_final_cutoff=int((inc.issued_date < cut).sum()), after_final_cutoff=int((inc.issued_date >= cut).sum()),
                posting_lag_days_median=float(lag.median()), posting_lag_days_iqr=[float(lag.quantile(.25)), float(lag.quantile(.75))],
                posting_lag_days_max=int(lag.max()),
                by_month_group=inc.groupby(['month', 'group']).size().unstack(fill_value=0).reindex(columns=ORDER, fill_value=0).to_dict(orient='index'),
                events=EVENTS,
                by_group_before_after={g: [int(((inc.group == g) & (inc.issued_date < cut)).sum()), int(((inc.group == g) & (inc.issued_date >= cut)).sum())] for g in ORDER})
json.dump(timeline, open(f'{RES}/timeline.json', 'w'), indent=1)

# ---------- telehealth-type waves (letters to telehealth platforms and clinics, by batch) ----------
W = {'2025-09-09': 'Sep 2025', '2026-02-20': 'Feb 2026', '2026-06-08': 'Jun 2026'}
wv = []
waves_df = inc[inc.issued_date.dt.strftime('%Y-%m-%d').isin(W)]
for d, lab in W.items():
    sub = waves_df[waves_df.issued_date.dt.strftime('%Y-%m-%d') == d]
    for c in ['V_misbrand_502bb', 'C_sameness', 'C_brand_names', 'C_fda_approved', 'C_firm_branded', 'C_generic', 'V_unapproved', 'V_other_peptide']:
        k = int(sub[c].sum()); lo, hi = wilson(k, len(sub))
        wv.append(dict(wave=lab, date=d, code=c, label=CODE_LABEL[c], n=k, N=len(sub), pct=k / len(sub), lo=lo, hi=hi))
wv = pd.DataFrame(wv); wv.to_csv(f'{RES}/waves.csv', index=False)

# ---------- close-outs ----------
clo = df[df.closeout_letter.notna()][['slug', 'company', 'issued', 'closeout_letter', 'eligible']]
closeouts = dict(n_closeout_all=int(len(clo)), n_closeout_included=int(clo.eligible.sum()), n_response_letters=int(df.response_letter.notna().sum()),
                 closeout_dates=clo.closeout_letter.tolist())

# ---------- recalls (openFDA enforcement) ----------
R = json.load(open(f'{RAW}/openfda_enforcement_glp1_2026-10-22.json'))
rec = {}
for t, q in R['queries'].items():
    for r in q['results']:
        rec[r['recall_number']] = r
rdf = pd.DataFrame(rec.values())
rdf['init'] = pd.to_datetime(rdf.recall_initiation_date, format='%Y%m%d')
rdf['steril'] = rdf.reason_for_recall.str.contains('steril', case=False)
recalls = dict(pulled=R['pulled'], totals={t: q['total'] for t, q in R['queries'].items()}, unique_recall_records=len(rdf),
               unique_events=int(rdf.event_id.nunique()), unique_firm_names=int(rdf.recalling_firm.nunique()),
               unique_firms_normalized=int(rdf.recalling_firm.str.lower().str.replace('acquisitions', 'acquisition').str.replace(r'[^a-z0-9 ]', '', regex=True).str.replace(r'\b(llc|inc|incorporated|corp|corporation|co|ltd)\b', '', regex=True).str.split().str.join(' ').nunique()),
               records_before_2023Q4=int((rdf.init < pd.Timestamp('2023-10-01')).sum()),
               by_year=rdf.init.dt.year.value_counts().sort_index().astype(int).to_dict(),
               by_quarter=rdf.init.dt.to_period('Q').astype(str).value_counts().sort_index().astype(int).to_dict(),
               sterility_records=int(rdf.steril.sum()), sterility_share=float(rdf.steril.mean()),
               by_quarter_sterility=rdf[rdf.steril].init.dt.to_period('Q').astype(str).value_counts().sort_index().astype(int).to_dict(),
               classification=rdf.classification.value_counts().to_dict())
recalls = {k: ({str(a): b for a, b in v.items()} if isinstance(v, dict) else v) for k, v in recalls.items()}
import hashlib
recalls['openfda_file_sha256'] = hashlib.sha256(open(f'{RAW}/openfda_enforcement_glp1_2026-10-22.json', 'rb').read()).hexdigest()
json.dump(recalls, open(f'{RES}/recalls.json', 'w'), indent=1)

# ---------- open dataset (public records; allegations only) ----------
od = df[['slug', 'url', 'company', 'issued', 'posted', 'office', 'subject', 'closeout_letter', 'text_sha256', 'raw_html_sha256',
         'eligible', 'exclusion', 'seller_type'] + CODES].copy()
od.to_csv(f'{RES}/open_dataset.csv', index=False)

summary = dict(N_included=N, seller_counts=seller_counts, group_counts=group_counts, products_named=prod, closeouts=closeouts,
               any_claim_502bb_sameness_fda=int(((inc.C_sameness == 1) | (inc.C_fda_approved == 1) | (inc.C_firm_branded == 1)).sum()),
               telehealth_like_502bb=int(inc[inc.group.isin(['Telehealth platform', 'Clinic / med spa'])].V_misbrand_502bb.sum()),
               telehealth_like_n=int(inc.group.isin(['Telehealth platform', 'Clinic / med spa']).sum()),
               n_502bb_outside_telehealth_like=int(inc[~inc.group.isin(['Telehealth platform', 'Clinic / med spa'])].V_misbrand_502bb.sum()),
               research_chem_with_other_peptide=int(inc[inc.seller_type == 'research_chem'].V_other_peptide.sum()),
               n_inspection_based=int(inc.F_inspection.sum()), n_website_based=int(inc.F_website_review.sum()))
json.dump(summary, open(f'{RES}/summary.json', 'w'), indent=1, default=int)
print(json.dumps(flow, indent=1)[:800]); print(json.dumps(summary, indent=1)); print(json.dumps({k: timeline[k] for k in ['by_year', 'batch_dates', 'batch_share', 'top3_share', 'before_final_cutoff', 'after_final_cutoff', 'posting_lag_days_median', 'by_group_before_after']}, indent=1))
print(prev[['code', 'n', 'pct']].to_string()); print(wv.pivot(index='code', columns='wave', values='pct').round(2)); print(json.dumps(recalls, indent=1)[:1500])

# ---------- sensitivity: prevalence under the rule-based coder alone (same included letters) ----------
p1 = pd.read_csv(f'{RES}/../data/coding/pass1_rules.csv').set_index('slug').loc[inc.slug]
sens = pd.DataFrame([dict(code=c, label=CODE_LABEL[c], n_final=int(inc[c].sum()), n_rules=int(p1[c].sum()), N=N) for c in CODES])
sens.to_csv(f'{RES}/sensitivity_rules_only.csv', index=False); print(sens.to_string())
