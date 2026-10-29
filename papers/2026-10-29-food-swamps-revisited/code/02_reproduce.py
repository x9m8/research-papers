"""Reproduction of Tables 3, 6, 7, 8 and 9 of Cooksey-Stowers, Schwartz & Brownell (2017).
Writes results/reproduction.json."""
import numpy as np, pandas as pd
from common import DER, CTRL, CTRL_NOTE, TARGET, dump
from econ import ols, iv

d = pd.read_csv(f'{DER}/county_base.csv')
d['rfei_alt'] = (d.convs + d.groc) / d.groc.where(d.groc > 0)          # hypothesised published 'traditional RFEI' (see text)
d['any_exit'] = (d.exits_osm > 0).astype(float)
d['log_exits'] = np.log1p(d.exits_osm)
S = d[d.natamen.notna() & d.obese.notna()].copy()                     # contiguous US: the Natural Amenities Index covers the lower 48 only
out = {'n_contig': len(S)}

# ---------- descriptive statistics, Table 3 comparison (all counties with data; medians and SDs)
pub3 = {'obese': (30.5, 4.16), 'recfac': (2.0, 30.31), 'natamen': (3.0, 1.04), 'ffr': (15.0, 228.60), 'groc': (6.0, 76.80),
        'superc': (0.0, 2.64), 'convs': (16.0, 87.50), 'specs': (1.0, 37.95), 'fmrkt': (1.0, 4.00), 'lila': (6.2, 8.37),
        'rfei_trad': (3.5, 1.86), 'rfei_e1': (3.4, 2.14), 'rfei_e2': (3.6, 2.38), 'ffr_pth': (5.8, 2.99), 'pct_black': (1.9, 14.42),
        'pct_hisp': (3.3, 13.20), 'medhhinc': (41255, 10742), 'pop65': (4000, 36536.21), 'povrate': (15.9, 6.24), 'pop10': (25970, 313819.30),
        'bach_only': (12.2, 5.35), 'pct_drovealone': (80.2, 7.79), 'pct_transit': (0.4, 3.07), 'pct_walk': (2.5, 3.75), 'gini': (0.4, 0.04),
        'exits_osm': (0.0, 33.51), 'milksoda': (30.2, 62.10), 'sqmi': (624.0, 1314.10)}
desc = {}
for v, (m, s) in pub3.items():
    x = d[v].replace([np.inf, -np.inf], np.nan).dropna()
    desc[v] = {'pub_median': m, 'pub_sd': s, 'median': x.median(), 'sd': x.std(), 'mean': x.mean(), 'n': len(x)}
for v in ['ffr_09', 'groc_09', 'superc_09', 'convs_09', 'specs_09', 'recfac_09', 'rfei_trad_09', 'rfei_e1_09', 'rfei_e2_09', 'rfei_alt']:
    x = d[v].replace([np.inf, -np.inf], np.nan).dropna(); desc[v] = {'median': x.median(), 'sd': x.std(), 'mean': x.mean(), 'n': len(x)}
desc['lila']['mean_note'] = 'published "(8.37)" equals the mean, not the SD'
out['table3'] = desc
out['table4_cutoffs'] = {k: {'mean_contig': S[k].mean(), 'n_above_pub_cut': int((S[k] > c).sum())}
                         for k, c in [('rfei_e1', 3.79), ('rfei_e2', 4.02), ('rfei_trad', 3.89), ('lila', 8.37), ('rfei_alt', 3.89)]}
out['table4_pub'] = {'rfei_e1': [3.79, 1470], 'rfei_e2': [4.02, 1425], 'rfei_trad': [3.89, 1419], 'lila': [8.37, 1193]}
out['ns'] = {k: int(S[k].notna().sum()) for k in ['rfei_trad', 'rfei_e1', 'rfei_e2', 'rfei_trad_09', 'rfei_e1_09', 'rfei_e2_09']}

# ---------- correlations (Table 5 and Table A3 items)
out['corr'] = {'lila_trad': S[['lila', 'rfei_trad']].corr().iloc[0, 1], 'lila_e1': S[['lila', 'rfei_e1']].corr().iloc[0, 1],
               'lila_e2': S[['lila', 'rfei_e2']].corr().iloc[0, 1]}
for v in ['obese', 'recfac', 'ffr', 'groc', 'convs', 'pop10', 'sqmi', 'rfei_trad', 'rfei_e1', 'rfei_e2', 'lila', 'bach_only', 'gini']:
    out['corr'][f'exits_{v}'] = S[['exits_osm', v]].corr().iloc[0, 1]
out['corr_pub'] = {'exits_obese': -0.20, 'exits_recfac': 0.84, 'exits_ffr': 0.86, 'exits_groc': 0.74, 'exits_convs': 0.86, 'exits_pop10': 0.86,
                   'exits_sqmi': 0.14, 'exits_rfei_trad': -0.07, 'exits_rfei_e1': 0.04, 'exits_rfei_e2': 0.05, 'lila_trad': -0.06, 'lila_e1': -0.10, 'lila_e2': -0.10}
out['exits'] = {'zero_contig': int((S.exits_osm == 0).sum()), 'zero_all': int((d.exits_osm == 0).sum()), 'pub_zero': 1672,
                'median': S.exits_osm.median(), 'sd': S.exits_osm.std(), 'mean': S.exits_osm.mean(), 'total_contig': S.exits_osm.sum()}

# ---------- OLS (Table 6) and IV (Tables 7-8)
def block(sfx='', ctrl=CTRL, z='exits_osm', data=S, keys=('e1', 'e2', 'trad')):
    r = {}
    for k in keys:
        x = f'rfei_{k}{sfx}' if k != 'alt' else 'rfei_alt'
        o_c = ols(data, 'obese', [x] + ctrl, kind='cluster'); o_h = ols(data, 'obese', [x] + ctrl, kind='hc1')
        i_c = iv(data, 'obese', x, z, ctrl, kind='cluster'); i_h = iv(data, 'obese', x, z, ctrl, kind='hc1', ar=True)
        r[k] = {'ols_b': o_c['b'][x], 'ols_se_cl': o_c['se'][x], 'ols_se_hc1': o_h['se'][x], 'ols_n': o_c['n'], 'ols_r2': o_c['r2'],
                'ols_ctrl': {c: [o_c['b'][c], o_c['se'][c]] for c in ['lila', 'recfac', 'natamen', 'milksoda', 'const']},
                'iv_b': i_c['b'], 'iv_se_cl': i_c['se'], 'iv_se_hc1': i_h['se'], 'iv_n': i_c['n'], 'iv_p_cl': i_c['p'],
                'fs_b': i_c['fs_b'], 'fs_se_cl': i_c['fs_se'], 'fs_F_cl': i_c['fs_F'], 'fs_F_hc1': i_h['fs_F'], 'fs_F_homo': i_c['fs_F_homo'],
                'rf_b': i_c['rf_b'], 'rf_se_cl': i_c['rf_se'], 'ar_cl': i_c['ar'], 'ar_hc1': i_h['ar'],
                'iv_ctrl': {c: [i_c['ctrl_b'][c], i_c['ctrl_se'][c]] for c in ['lila', 'recfac', 'natamen', 'milksoda', 'const']}}
    return r
out['main'] = block()                               # 2007 counts, matched control set, OSM exits
out['main_alt'] = block(keys=('alt',))              # hypothesised published traditional-RFEI construction
out['counts2009'] = block('_09')                    # 2009 counts, as the paper describes its data
out['note_controls'] = block(ctrl=CTRL_NOTE)        # literal control list from the table notes
out['uniqref_instrument'] = block(z='exits_osm_uniqref')

# ---------- Table 9: stratified IV, traditional RFEI, matched controls
strat = {}
for nm, mask in [('commute<80', S.pct_drive_transit < 80), ('commute>80', S.pct_drive_transit >= 80),
                 ('gini<0.41', S.gini < 0.41), ('gini>0.41', S.gini >= 0.41),
                 ('gini<median', S.gini < S.gini.median()), ('gini>median', S.gini >= S.gini.median())]:
    sub = S[mask]
    for x in ['rfei_trad', 'rfei_alt']:
        r = iv(sub, 'obese', x, 'exits_osm', CTRL, kind='cluster')
        strat[f'{nm}|{x}'] = {'b': r['b'], 'se': r['se'], 'n': r['n'], 'fs_F': r['fs_F'], 'ar': r['ar'], 'p': r['p']}
    strat[f'{nm}|n_sample'] = int(mask.sum())
out['strat'] = strat
out['strat_gini_cut_for_2442'] = float(np.sort(S.loc[S.rfei_trad.notna(), 'gini'])[2441])

# ---------- interpretation of the coefficient
T = S[S.rfei_trad.notna()]
sd = T.rfei_trad.std()
one_pct = 0.01 * T.ffr / T.groc            # change in the traditional RFEI from a 1% rise in fast-food outlets
interp = {'sd_rfei_trad': sd, 'sd_obese': T.obese.std(), 'median_dRFEI_1pct_ffr': one_pct.median(), 'mean_dRFEI_1pct_ffr': one_pct.mean()}
for lab, b in [('pub_ols', 0.125), ('our_ols', out['main']['trad']['ols_b']), ('pub_iv', 2.604)]:
    interp[lab] = {'beta': b, 'pp_per_1pct_ffr_median': b * one_pct.median(), 'pp_per_1pct_ffr_mean': b * one_pct.mean(),
                   'pp_per_sd': b * sd, 'elasticity_at_means': b * (T.ffr / T.groc).mean() / T.obese.mean() * 1.0}
# 'about three percent' in the Discussion: RFEI reduction implied by 3 points at beta = 2.604
need = 3 / 2.604
interp['sd_rfei_alt'] = S.loc[S.rfei_alt.notna(), 'rfei_alt'].std()
interp['pub_iv_pp_per_sd_alt'] = 2.604 * interp['sd_rfei_alt']
interp['mean_obese'] = T.obese.mean(); interp['three_pct_relative_pp'] = 0.03 * T.obese.mean()
interp['zoning'] = {'rfei_units_for_3pp': need, 'median_outlets_removed': (need * T.groc).median(),
                    'median_share_of_unhealthy_outlets_removed': (need * T.groc / (T.ffr + T.convs)).median(),
                    'share_counties_rfei_below_need': float((T.rfei_trad < need).mean()),
                    'pub_iv_pp_per_sd': 2.604 * sd}
out['interp'] = interp
dump(out, 'reproduction.json')
m = out['main']
for k in ('e1', 'e2', 'trad'):
    print(k, {kk: (round(v, 4) if isinstance(v, float) else v) for kk, v in m[k].items() if kk in ('ols_b', 'ols_se_cl', 'ols_n', 'ols_r2', 'iv_b', 'iv_se_cl', 'fs_b', 'fs_F_cl', 'fs_F_hc1', 'ar_cl')})
print('alt', {kk: v for kk, v in out['main_alt']['alt'].items() if kk in ('ols_b', 'ols_se_cl', 'iv_b', 'iv_se_cl', 'fs_F_cl', 'ar_cl')})
print(out['exits']); print({k: round(v, 3) for k, v in out['corr'].items()})
print({k: v for k, v in strat.items()})
print(interp)
