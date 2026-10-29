"""Robustness grid for the food-swamp coefficient (OLS and IV), zero-denominator handling, state fixed effects,
alternative instrument codings, population weights, size controls. Writes results/robustness.json and robustness.csv."""
import numpy as np, pandas as pd
from common import DER, RES, CTRL, dump
from econ import ols, iv

d = pd.read_csv(f'{DER}/county_base.csv')
d['any_exit'] = (d.exits_osm > 0).astype(float); d['log_exits'] = np.log1p(d.exits_osm)
d['exits_per_1000sqmi'] = 1000 * d.exits_osm / d.sqmi; d['lpop'] = np.log(d.pop10.fillna(d.pop_acs))
d['pop10k'] = d.pop10.fillna(d.pop_acs) / 1e4; d['pop65k'] = d.pop65 / 1e3
S = d[d.natamen.notna() & d.obese.notna()].copy()
for k in ('trad', 'e1', 'e2'):
    q = S[f'rfei_{k}'].quantile(0.99); S[f'rfei_{k}_trim'] = S[f'rfei_{k}'].where(S[f'rfei_{k}'] <= q)

rows = []
def run(label, group, x, data=S, ctrl=CTRL, z='exits_osm', fe=None, w=None, scale=1.0):
    o = ols(data, 'obese', [x] + ctrl, kind='cluster', fe=fe, w=w)
    r = iv(data, 'obese', x, z, ctrl, kind='cluster', fe=fe, w=w)
    rows.append({'label': label, 'group': group, 'x': x, 'z': z, 'fe': fe or '', 'w': w or '',
                 'ols_b': o['b'][x] * scale, 'ols_se': o['se'][x] * scale, 'n': o['n'],
                 'iv_b': r['b'] * scale, 'iv_se': r['se'] * scale, 'fs_F': r['fs_F'], 'fs_b': r['fs_b'],
                 'ar_type': r['ar']['type'], 'ar_lo': (r['ar']['lo'] * scale if r['ar']['lo'] is not None else None),
                 'ar_hi': (r['ar']['hi'] * scale if r['ar']['hi'] is not None else None), 'rf_b': r['rf_b'], 'rf_se': r['rf_se']})

for k in ('trad', 'e1', 'e2'):
    x = f'rfei_{k}'
    run('Baseline (2007 counts, matched controls, clustered SE)', k, x)
    run('State fixed effects', k, x, fe='stfips')
    run('Add people over 65 (count, as in the table notes)', k, x, ctrl=CTRL + ['pop65k'])
    run('Add population (linear)', k, x, ctrl=CTRL + ['pop10k'])
    run('Add population (linear) + state fixed effects', k, x, ctrl=CTRL + ['pop10k'], fe='stfips')
    run('Add log population', k, x, ctrl=CTRL + ['lpop'])
    run('Add log population + state fixed effects', k, x, ctrl=CTRL + ['lpop'], fe='stfips')
    run('Add log and linear population', k, x, ctrl=CTRL + ['lpop', 'pop10k'])
    run('Population-weighted', k, x, w='pop10')
    run('Zero denominators kept: (num+1)/(den+1)', k, f'rfei_{k}_p1')
    run('Log of (num+1)/(den+1)', k, f'lrfei_{k}')
    run('Drop top 1% of RFEI', k, f'rfei_{k}_trim')
    run('Drop counties with denominator < 3', k, x, data=S[S[f'den_{k}'] >= 3])
    run('Instrument: any exit (0/1)', k, x, z='any_exit')
    run('Instrument: log(1 + exits)', k, x, z='log_exits')
    run('Instrument: exits per 1,000 sq mi', k, x, z='exits_per_1000sqmi')
    run('Instrument: distinct exit refs', k, x, z='exits_osm_uniqref')
    run('Counties with at least one exit', k, x, data=S[S.exits_osm > 0])
    run('2009 store counts', k, f'rfei_{k}_09')
R = pd.DataFrame(rows); R.to_csv(f'{RES}/robustness.csv', index=False)

# per-capita densities instead of a ratio (separate coefficients for unhealthy and healthy outlets per 10,000 people)
dens = {}
for lab, fe in [('no FE', None), ('state FE', 'stfips')]:
    o = ols(S, 'obese', ['unh_pth', 'hea_pth'] + CTRL, kind='cluster', fe=fe)
    dens[lab] = {'unh_b': o['b']['unh_pth'], 'unh_se': o['se']['unh_pth'], 'hea_b': o['b']['hea_pth'], 'hea_se': o['se']['hea_pth'], 'n': o['n']}
# placebo-style check: does the instrument predict obesity conditional on the RFEI (direct path)?
o = ols(S, 'obese', ['exits_osm', 'rfei_trad'] + CTRL, kind='cluster')
direct = {'exits_b': o['b']['exits_osm'], 'exits_se': o['se']['exits_osm'], 'n': o['n']}
# correlation of the people-over-65 count with population
pop_corr = S[['pop65', 'pop10']].corr().iloc[0, 1]
o2 = ols(S, 'recfac', ['exits_osm'] + [c for c in CTRL if c != 'recfac'], kind='cluster')
dump({'grid': R.to_dict(orient='records'), 'densities': dens, 'direct_path': direct,
      'exits_on_recfac': {'b': o2['b']['exits_osm'], 'se': o2['se']['exits_osm']}, 'corr_pop65_pop': pop_corr}, 'robustness.json')
pd.set_option('display.width', 250); print(R[['label', 'group', 'ols_b', 'ols_se', 'n', 'iv_b', 'iv_se', 'fs_F', 'ar_type', 'ar_lo', 'ar_hi']].round(3).to_string())
print(dens, direct)
