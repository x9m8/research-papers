"""Update with newer data: (a) 2016 store counts with PLACES model-based obesity for BRFSS 2018 (cross-section,
OLS and IV), (b) county long difference 2007/2009 -> 2016/2018. Writes results/update.json."""
import numpy as np, pandas as pd
from common import DER, CTRL, dump
from econ import ols, iv

b = pd.read_csv(f'{DER}/county_base.csv'); u = pd.read_csv(f'{DER}/county2016.csv')
u = u[u.natamen.notna() & u.obese.notna()].copy()
u['lpop'] = np.log(u.pop_acs)
out = {'n_2016_contig': len(u), 'n_any_na16': int(u.any_na16.sum())}
cs = {}
for k in ('trad', 'e1', 'e2'):
    x = f'rfei_{k}'
    for lab, data, fe, ctrl in [('all', u, None, CTRL), ('state FE', u, 'stfips', CTRL), ('no -9999 counts', u[~u.any_na16.astype(bool)], None, CTRL),
                                ('add log pop + state FE', u, 'stfips', CTRL + ['lpop'])]:
        o = ols(data, 'obese', [x] + ctrl, kind='cluster', fe=fe); r = iv(data, 'obese', x, 'exits_osm', ctrl, kind='cluster', fe=fe)
        cs[f'{k}|{lab}'] = {'ols_b': o['b'][x], 'ols_se': o['se'][x], 'n': o['n'], 'r2': o['r2'], 'iv_b': r['b'], 'iv_se': r['se'],
                            'fs_F': r['fs_F'], 'ar': r['ar']}
out['cross_section_2016'] = cs

# long difference: change in obesity (PLACES 2018 minus Atlas/CDC 2009) on change in RFEI (2016 minus 2007)
m = b[b.natamen.notna()].merge(u[['fips', 'obese', 'rfei_trad', 'rfei_e1', 'rfei_e2', 'unh_pth', 'hea_pth', 'any_na16', 'povrate', 'bach_only']],
                                on='fips', suffixes=('', '_16'))
m['d_obese'] = m.obese_16 - m.obese
for k in ('trad', 'e1', 'e2'): m[f'd_rfei_{k}'] = m[f'rfei_{k}_16'] - m[f'rfei_{k}']
m['d_unh'] = m.unh_pth_16 - m.unh_pth; m['d_hea'] = m.hea_pth_16 - m.hea_pth
m['d_pov'] = m.povrate_16 - m.povrate; m['d_bach'] = m.bach_only_16 - m.bach_only
ld = {'corr_rfei_trad_07_16': m[['rfei_trad', 'rfei_trad_16']].corr().iloc[0, 1], 'corr_rfei_e1_07_16': m[['rfei_e1', 'rfei_e1_16']].corr().iloc[0, 1],
      'corr_rfei_e2_07_16': m[['rfei_e2', 'rfei_e2_16']].corr().iloc[0, 1], 'mean_d_obese': m.d_obese.mean(), 'sd_d_obese': m.d_obese.std(), 'corr_obese_levels': m[['obese', 'obese_16']].corr().iloc[0, 1]}
for k in ('trad', 'e1', 'e2'):
    x = f'd_rfei_{k}'
    for lab, data, ctrl in [('state FE', m, CTRL), ('state FE + changes in poverty and education', m, CTRL + ['d_pov', 'd_bach']),
                            ('state FE, no -9999 counts', m[~m.any_na16.astype(bool)], CTRL)]:
        o = ols(data, 'd_obese', [x] + ctrl, kind='cluster', fe='stfips')
        ld[f'{k}|{lab}'] = {'b': o['b'][x], 'se': o['se'][x], 'n': o['n'], 'sd_x': data[x].std()}
o = ols(m, 'd_obese', ['d_unh', 'd_hea'] + CTRL, kind='cluster', fe='stfips')
ld['densities|state FE'] = {'unh_b': o['b']['d_unh'], 'unh_se': o['se']['d_unh'], 'hea_b': o['b']['d_hea'], 'hea_se': o['se']['d_hea'], 'n': o['n']}
out['long_difference'] = ld
dump(out, 'update.json')
for k, v in cs.items(): print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()})
for k, v in ld.items(): print(k, v)
