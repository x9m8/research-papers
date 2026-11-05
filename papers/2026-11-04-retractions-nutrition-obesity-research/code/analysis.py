"""Step 2: counts over time, reasons, time to retraction, countries, publishers; field vs rest of database; sensitivity to the
field definition. Reads data/derived/records.csv; writes results/trends.json, comparison.json, sensitivity.json."""
import os, math, collections
import numpy as np, pandas as pd
from common import *

r = pd.read_csv(os.path.join(DER, 'records.csv'), dtype={'Record ID': str, 'doi': str, 'Country': str}, keep_default_na=False,
                na_values={'ret_year': [''], 'pub_year': [''], 'ttr_days': ['']})
for c in ['S', 'J', 'F', 'K', 'primary', 'broad', 'biomed', 'glp1', 'conference', 'date_unknown'] + [c for c in r.columns if c.startswith('g_')]:
    r[c] = r[c].astype(str).eq('True')
rng = np.random.default_rng(SEED)
GROUPS = ['misconduct', 'fabrication', 'plagiarism', 'duplication', 'paper_mill', 'peer_review', 'computer_generated', 'image',
          'forged_authorship', 'error', 'error_only', 'data_concerns', 'ethics_consent', 'authorship_dispute', 'publisher_error', 'limited_info',
          'misconduct_broad', 'referencing']
countries = r['Country'].map(lambda v: set(split(v)))
ttr_y = r['ttr_days'] / 365.25


def wilson(k, n, z=1.959964):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def newcombe(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2; l1, u1 = wilson(k1, n1); l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return (d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def prop(mask, comp, col):
    k1, n1, k2, n2 = int((mask & col).sum()), int(mask.sum()), int((comp & col).sum()), int(comp.sum())
    lo, hi = newcombe(k1, n1, k2, n2)
    return {'k': k1, 'n': n1, 'p': k1 / n1, 'k_comp': k2, 'n_comp': n2, 'p_comp': k2 / n2, 'diff': k1 / n1 - k2 / n2, 'diff_lo': lo, 'diff_hi': hi}


def ttr_stats(mask):
    x = ttr_y[mask].dropna().to_numpy()
    if len(x) == 0: return {'n': 0}
    q = np.percentile(x, [25, 50, 75])
    return {'n': int(len(x)), 'median': float(q[1]), 'q1': float(q[0]), 'q3': float(q[2]), 'mean': float(x.mean()),
            'within_1y': float((x < 1).mean()), 'over_5y': float((x > 5).mean())}


def median_diff_ci(mask, comp, B=2000):
    a, b = ttr_y[mask].dropna().to_numpy(), ttr_y[comp].dropna().to_numpy()
    d = np.empty(B)
    for i in range(B):
        d[i] = np.median(rng.choice(a, len(a))) - np.median(rng.choice(b, len(b)))
    return {'diff': float(np.median(a) - np.median(b)), 'lo': float(np.percentile(d, 2.5)), 'hi': float(np.percentile(d, 97.5))}


def country_share(mask, c):
    sub = countries[mask]
    return float(sub.map(lambda s: c in s).mean())


def compare(mask, comp, label, full=True):
    out = {'label': label, 'n': int(mask.sum()), 'n_comp': int(comp.sum()),
           'reasons': {g: prop(mask, comp, r['g_' + g]) for g in GROUPS},
           'ttr': ttr_stats(mask), 'ttr_comp': ttr_stats(comp),
           'recent_2023': prop(mask, comp, r['ret_year'] >= 2023), 'recent_2020': prop(mask, comp, r['ret_year'] >= 2020),
           'conference': prop(mask, comp, r['conference'])}
    for c in ['China', 'United States', 'India', 'Iran', 'Japan', 'Saudi Arabia']:
        out['country_' + c] = prop(mask, comp, countries.map(lambda s, c=c: c in s))
    if full:
        out['ttr_median_diff'] = median_diff_ci(mask, comp)
    return out


P, ALL = r['primary'], pd.Series(True, index=r.index)
REST, BIOREST = ~P, r['biomed'] & ~P

# ---- trends -------------------------------------------------------------------------------------------------------
years = list(range(1990, 2027))
tr = {}
for nm, m in [('all', ALL), ('biomed', r['biomed']), ('primary', P), ('broad', r['broad']), ('S', r['S']), ('J', r['J']), ('K', r['K'])]:
    vc = r.loc[m, 'ret_year'].value_counts()
    tr[nm] = [int(vc.get(y, 0)) for y in years]
    vp = r.loc[m, 'pub_year'].value_counts()
    tr['pub_' + nm] = [int(vp.get(y, 0)) for y in years]
tr['years'] = years
tr['n_ret_year_missing'] = int(r['ret_year'].isna().sum())
tr['primary_share_by_year'] = [tr['primary'][i] / tr['all'][i] if tr['all'][i] else None for i in range(len(years))]
# primary reasons by retraction year (for figure): paper mill/peer review/computer-generated vs other misconduct vs error-only
bulk = r['g_paper_mill'] | r['g_peer_review'] | r['g_computer_generated']
tr['primary_bulk'] = [int((P & bulk & (r['ret_year'] == y)).sum()) for y in years]
tr['all_bulk'] = [int((bulk & (r['ret_year'] == y)).sum()) for y in years]
tr['primary_hindawi'] = [int((P & r['Publisher'].eq('Hindawi') & (r['ret_year'] == y)).sum()) for y in years]
dump(tr, 'trends.json')

# ---- main comparison ----------------------------------------------------------------------------------------------
comp = {'primary_vs_rest': compare(P, REST, 'Nutrition/obesity (S or J) vs rest of database'),
        'primary_vs_biomed_rest': compare(P, BIOREST, 'Nutrition/obesity vs rest of biomedical (BLS/HSC subject)'),
        'primary_vs_rest_journal_only': compare(P & ~r['conference'], REST & ~r['conference'], 'Excluding conference papers', full=False)}
# v2 (after audit): conference papers excluded from both sides, with the bootstrap interval for the median time to retraction;
# the same against the rest of biomedicine; and Hindawi excluded from both sides.
NC = ~r['conference']; H = r['Publisher'].eq('Hindawi')
comp['journal_only_vs_rest'] = compare(P & NC, REST & NC, 'Journal articles only (conference papers excluded from both sides)')
comp['journal_only_vs_biomed_rest'] = compare(P & NC, BIOREST & NC, 'Journal articles only vs rest of biomedical')
comp['no_hindawi_vs_rest'] = compare(P & ~H, REST & ~H, 'Hindawi excluded from both sides')
eras = {'to2009': r['ret_year'] <= 2009, '2010_2019': r['ret_year'].between(2010, 2019), '2020_2026': r['ret_year'] >= 2020}
comp['by_era'] = {e: compare(P & m, REST & m, e, full=False) for e, m in eras.items()}
comp['by_era_journal_only'] = {e: compare(P & m & NC, REST & m & NC, e, full=False) for e, m in eras.items()}
# countries: top 15 by primary count
cc = collections.Counter(c for s in countries[P] for c in s)
comp['countries_top'] = [{'country': c, 'k': k, 'p': k / int(P.sum()), 'p_rest': country_share(REST, c), 'p_biomed_rest': country_share(BIOREST, c)}
                         for c, k in cc.most_common(15)]
comp['n_countries_primary'] = len(cc)
comp['publishers_primary'] = [{'publisher': p, 'k': int(k), 'p': int(k) / int(P.sum())} for p, k in r.loc[P, 'Publisher'].value_counts().head(10).items()]
comp['publishers_rest'] = [{'publisher': p, 'k': int(k), 'p': int(k) / int(REST.sum())} for p, k in r.loc[REST, 'Publisher'].value_counts().head(10).items()]
comp['ttr_by_era'] = {e: {'primary': ttr_stats(P & m), 'rest': ttr_stats(REST & m)} for e, m in eras.items()}
comp['ttr_by_reason_primary'] = {g: ttr_stats(P & r['g_' + g]) for g in ['misconduct', 'fabrication', 'paper_mill', 'peer_review', 'duplication', 'plagiarism', 'error_only']}
comp['ttr_by_reason_rest'] = {g: ttr_stats(REST & r['g_' + g]) for g in ['misconduct', 'fabrication', 'paper_mill', 'peer_review', 'duplication', 'plagiarism', 'error_only']}
# GLP-1 / anti-obesity drug subgroup (titles, whole database)
G = r['glp1']
comp['glp1'] = {'n': int(G.sum()), 'n_primary': int((G & P).sum()),
                'years': {str(int(k)): int(v) for k, v in r.loc[G, 'ret_year'].value_counts().sort_index().items()},
                'reasons': {g: int((G & r['g_' + g]).sum()) for g in GROUPS}, 'ttr': ttr_stats(G),
                'publishers': r.loc[G, 'Publisher'].value_counts().head(5).to_dict(),
                'china': int(countries[G].map(lambda s: 'China' in s).sum())}
dump(comp, 'comparison.json')

# ---- sensitivity to the field definition ------------------------------------------------------------------------------
defs = {'primary (S or J)': P, 'S: subject code only': r['S'], 'J: journal title only': r['J'], 'K: article title only': r['K'],
        'broad (S or J or K)': r['broad'], 'primary + food-science journals': P | r['F'],
        'primary, excluding conference papers': P & ~r['conference'],
        'primary, excluding Hindawi': P & ~r['Publisher'].eq('Hindawi'),
        'S and J (both)': r['S'] & r['J']}
sens = {}
for nm, m in defs.items():
    c = compare(m, ~m, nm, full=False)
    sens[nm] = {'n': c['n'], 'misconduct': c['reasons']['misconduct'], 'paper_mill': c['reasons']['paper_mill'],
                'peer_review': c['reasons']['peer_review'], 'error_only': c['reasons']['error_only'],
                'fabrication': c['reasons']['fabrication'], 'duplication': c['reasons']['duplication'],
                'limited_info': c['reasons']['limited_info'],
                'ttr': c['ttr'], 'ttr_comp': c['ttr_comp'], 'recent_2023': c['recent_2023'], 'china': c['country_China'],
                'us': c['country_United States'], 'misconduct_broad': c['reasons']['misconduct_broad']}
    cj = compare(m & NC, ~m & NC, nm + ' | journal articles only', full=False)
    sens[nm]['journal_only'] = {k: cj['reasons'][k] for k in ['misconduct', 'misconduct_broad', 'paper_mill', 'peer_review', 'error_only', 'limited_info']}
    sens[nm]['journal_only'].update({'n': cj['n'], 'n_comp': cj['n_comp'], 'ttr': cj['ttr'], 'ttr_comp': cj['ttr_comp'], 'china': cj['country_China'],
                                     'us': cj['country_United States'], 'recent_2023': cj['recent_2023']})
dump(sens, 'sensitivity.json')
print('analysis done', int(P.sum()))
