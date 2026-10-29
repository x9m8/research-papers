"""Derived quantities quoted in the text (ratios to the household-panel benchmark, national uptake) -> results/bounds.json."""
import json
from common import RES

E = json.load(open(f'{RES}/estimates.json')); B = json.load(open(f'{RES}/build.json')); D = json.load(open(f'{RES}/descriptives.json'))
est, bm = E['estimates'], E['benchmark_pct_per_pp']
nat = D['national']
out = {'national_E_2019': nat['2019']['E_national_approx'], 'national_E_2024': nat['2024']['E_national_approx'],
       'national_dE_2019_2024': nat['2024']['E_national_approx'] - nat['2019']['E_national_approx'],
       'national_fills_ratio_2024_2019': nat['2024']['fills_national'] / nat['2019']['fills_national'],
       'semtir_share_2024': nat['2024']['semtir_fills'] / nat['2024']['fills_national'],
       'semtir_share_2019': nat['2019']['semtir_fills'] / nat['2019']['fills_national'],
       'npi_coverage_2019': B['coverage']['2019']['share_of_national_in_npi_file'], 'npi_coverage_2024': B['coverage']['2024']['share_of_national_in_npi_file'],
       'match_min': min(c['share_fills_matched_to_county'] for c in B['coverage'].values()),
       'match_max': max(c['share_fills_matched_to_county'] for c in B['coverage'].values()),
       'state_corr_min': min(c['state_corr_county_sum_vs_cms_state'] for c in B['coverage'].values())}
for k in ('lsr_emp', 'diff_emp', 'fsr_emp'):
    m = est[k]['main']
    out[k] = {'lo_over_bench_m1': m['lo_pp'] / bm['m1'], 'lo_over_bench_m4': m['lo_pp'] / bm['m4'],
              'mde_over_bench_m1': m['mde_pp'] / abs(bm['m1']), 'mde_over_bench_m4': m['mde_pp'] / abs(bm['m4']),
              # implied by the benchmark for a county 1 SD above the mean in the change in uptake
              'bench_per_sd_m1': bm['m1'] * m['sd_x'], 'bench_per_sd_m4': bm['m4'] * m['sd_x'],
              # benchmark times the national 2019-2024 change (Part D uptake only)
              'bench_national_m1': bm['m1'] * out['national_dE_2019_2024'], 'bench_national_m4': bm['m4'] * out['national_dE_2019_2024']}
json.dump(out, open(f'{RES}/bounds.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
