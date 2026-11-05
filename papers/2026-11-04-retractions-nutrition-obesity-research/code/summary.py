"""Derived numbers quoted in the text -> results/summary.json (run locally from the verified result files)."""
import json
from common import RES, dump
S = json.load(open(f'{RES}/selection.json')); T = json.load(open(f'{RES}/trends.json')); C = json.load(open(f'{RES}/comparison.json'))
Y = T['years']
def tot(key, a, b): return sum(T[key][Y.index(a):Y.index(b) + 1])
out = {
    'primary_share_of_all': S['n_primary'] / S['n_retractions'],
    'primary_share_of_biomed': S['n_primary'] / S['n_biomed'],   # primary records are not all biomedical-coded; descriptive ratio only
    'primary_2000_2009': tot('primary', 2000, 2009), 'primary_2010_2019': tot('primary', 2010, 2019), 'primary_2020_2026': tot('primary', 2020, 2026),
    'primary_2023_2024': tot('primary', 2023, 2024), 'all_2023_2024': tot('all', 2023, 2024),
    'primary_2023': T['primary'][Y.index(2023)], 'primary_2024': T['primary'][Y.index(2024)], 'primary_2025': T['primary'][Y.index(2025)],
    'primary_2026_partial': T['primary'][Y.index(2026)],
    'primary_hindawi_2023': T['primary_hindawi'][Y.index(2023)], 'primary_bulk_2023': T['primary_bulk'][Y.index(2023)],
    'primary_bulk_2024': T['primary_bulk'][Y.index(2024)], 'primary_hindawi_2024': T['primary_hindawi'][Y.index(2024)],
    'primary_bulk_2023_2024': tot('primary_bulk', 2023, 2024), 'primary_bulk_total': sum(T['primary_bulk']),
    'all_2023': T['all'][Y.index(2023)],
    'broad_2023': T['broad'][Y.index(2023)],
    'share_by_year_2017': T['primary_share_by_year'][Y.index(2017)], 'share_by_year_2023': T['primary_share_by_year'][Y.index(2023)],
    'share_by_year_2024': T['primary_share_by_year'][Y.index(2024)],
    'K_only': S['venn']['S0J0K1'], 'S_only': S['venn']['S1J0K0'], 'J_only': S['venn']['S0J1K0'],
    'primary_years_before_1990': S['n_primary'] - sum(T['primary']),
}
# conference retractions in the rest of the database: share citing a misconduct reason (all-records minus journal-only comparison)
a, j = C['primary_vs_rest']['reasons']['misconduct'], C['journal_only_vs_rest']['reasons']['misconduct']
out['rest_conference_n'] = a['n_comp'] - j['n_comp']; out['rest_conference_misconduct_k'] = a['k_comp'] - j['k_comp']
out['rest_conference_misconduct_share'] = out['rest_conference_misconduct_k'] / out['rest_conference_n']
U = json.load(open(f'{RES}/unmapped_reasons.json'))
inv = [x for x in U['unmapped'] if x['reason'] == 'Investigation by Journal/Publisher'][0]
out['investigation_journal_primary_share'] = inv['k_primary'] / U['n_primary']; out['investigation_journal_rest_share'] = inv['k_rest'] / U['n_rest']
dump(out, 'summary.json'); print(out)
