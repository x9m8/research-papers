"""Robustness of the 1974-2003 result to inputs and assumptions. Each row: waste and share of supply wasted in 1974 and 2003."""
import numpy as np, pandas as pd
from common import *

fa = pd.read_csv(f'{DER}/fa.csv', index_col=0); P = pd.read_csv(f'{DER}/bw_points.csv'); I = load('inputs.json')
A, E = load_nhanes(); O = load_ogden()
YRS = np.arange(1974, 2004); i3 = len(YRS) - 1
pts = {s: list(zip(g.t, g.bw)) for s, g in P.groupby('series')}
FA = fa.loc[YRS, 'fbsh'].values

def summarize(label, Iy, note='', FAy=FA):
    w = FAy - Iy; fr = w / FAy
    return {'label': label, 'I_2003': Iy[i3], 'dI_2003': Iy[i3] - Iy[0], 'waste_1974': w[0], 'waste_2003': w[i3], 'increase_pct': 100 * (w[i3] / w[0] - 1),
            'frac_1974': 100 * fr[0], 'frac_2003': 100 * fr[i3], 'change_pp': 100 * (fr[i3] - fr[0]), 'note': note}

rows = []
base = intake(pts['nchs'], YRS, NOMINAL, F0_HALL)['I']
rows.append(summarize('Baseline: NCHS body weights, current FAO (FBSH), nominal parameters', base))
rows.append(summarize('Body weights digitized from the original Figure 1A', intake(pts['hall_digitized'], YRS, NOMINAL, F0_HALL)['I']))
rows.append(summarize('γF = 3.6 (Table 1) instead of 3.2 (text)', intake(pts['nchs'], YRS, {**NOMINAL, 'gF': 3.6}, F0_HALL)['I']))
rows.append(summarize(f"F0 = {I['F0']['nhanes1_calibrated']:.1f} kg (re-derived from NHANES I) instead of 19.1", intake(pts['nchs'], YRS, NOMINAL, I['F0']['nhanes1_calibrated'])['I']))
rows.append(summarize('Body weights: adults 20+ incl. pregnant (NHANES III onward)', intake(pts['nchs_20p'], YRS, NOMINAL, F0_HALL)['I']))
rows.append(summarize('Body weights: survey-weighted female share (1999 onward)', intake(pts['nchs_wshare'], YRS, NOMINAL, F0_HALL)['I']))
# survey points placed at end years
end_pts = []
for t, b in pts['nchs']:
    t2 = {1974.0: 1974.0, 1978.5: 1980.0, 1991.0: 1994.0}.get(t, t + 0.5)
    end_pts.append((t2, b))
rows.append(summarize('Survey points at end years (NHANES II 1980, III 1994, cycles +0.5 y)', intake(end_pts, YRS, NOMINAL, F0_HALL)['I']))
# baseline intake
for lab, v in (('IOM sedentary, NHANES I means', I['I0_iom']['sedentary|age+0']), ('IOM low-active, NHANES I means', I['I0_iom']['low_active|age+0'])):
    rows.append(summarize(f'I0 = {v:,.0f} kcal/d ({lab})', intake(pts['nchs'], YRS, {**NOMINAL, 'I0': v}, F0_HALL)['I']))
sr = (1 - P_W) * 2450 + P_W * 1542
rows.append(summarize(f'I0 = {sr:,.0f} kcal/d (self-reported, NHANES I, Wright et al., 2004)', intake(pts['nchs'], YRS, {**NOMINAL, 'I0': sr}, F0_HALL)['I'],
                      'self-report is known to understate intake'))
# physical activity falls 10% between 1974 and 2003
dpath = NOMINAL['delta'] * (1 - 0.10 * (YRS - 1974) / (2003 - 1974))
rows.append(summarize('Physical activity coefficient falls 10% by 2003', intake(pts['nchs'], YRS, NOMINAL, F0_HALL, delta_path=dpath)['I']))
dpath2 = NOMINAL['delta'] * (1 + 0.10 * (YRS - 1974) / (2003 - 1974))
rows.append(summarize('Physical activity coefficient rises 10% by 2003', intake(pts['nchs'], YRS, NOMINAL, F0_HALL, delta_path=dpath2)['I']))
# whole-population intake: children eat less than adults
ratio = E.set_index('cycle').loc['1999-2000']; r99 = ratio.eer_sed_all / ratio.eer_sed_2074
rows.append(summarize(f'Per-capita intake = adult intake × {r99:.3f} (IOM requirement, all ages / adults, NHANES 1999–2000)', base * r99,
                      'ratio held at its 1999-2000 value for all years'))
# requirement-based intake (IOM, sedentary and low-active, PAL fixed): no energy-balance model
og = O[O.ages == '20-74']
ages99 = {int(k): v for k, v in I['I0_ages_used'].items()}
def eer(sex, age, wt, htm, pa):
    return 662 - 9.53 * age + pa * (15.91 * wt + 539.6 * htm) if sex == 1 else 354 - 6.91 * age + pa * (9.36 * wt + 726 * htm)
def eer_pts(pa):
    out = []
    for s, t in (('NHANES I', 1974.0), ('NHANES II', 1978.5), ('NHANES III', 1991.0)):
        v = [eer(sx, ages99[sx], og[(og.survey == s) & (og.sex == sx)].iloc[0].wt_kg, og[(og.survey == s) & (og.sex == sx)].iloc[0].ht_cm / 100, pa[sx - 1]) for sx in (1, 2)]
        out.append((t, (1 - P_W) * v[0] + P_W * v[1]))
    for cyc, t in (('1999-2000', 1999.5), ('2001-2002', 2001.5), ('2003-2004', 2003.5)):
        v = []
        for sx in (1, 2):
            r = A[(A.cycle == cyc) & (A.sex == sx) & (A.ages == '2074') & (A.pregnant == 'excl')].iloc[0]
            v.append(eer(sx, ages99[sx], r.wt_kg, r.ht_cm / 100, pa[sx - 1]))   # age held at 1999-2000 means
        out.append((t, (1 - P_W) * v[0] + P_W * v[1]))
    return out
for lab, pa in (('sedentary', (1.0, 1.0)), ('low-active', (1.11, 1.12))):
    ep = eer_pts(pa); e = np.interp(YRS, *zip(*ep)); Ireq = NOMINAL['I0'] + (e - e[0])
    rows.append(summarize(f'Steady-state requirement (IOM, {lab}) instead of the energy-balance model', Ireq,
                          f'intake change = change in IOM EER at fixed age; dEER 1974-2003 = {e[-1]-e[0]:.0f} kcal/d'))
# combined: low-active baseline + children adjustment
rows.append(summarize('Combined: per-capita adjustment and IOM low-active I0', intake(pts['nchs'], YRS, {**NOMINAL, 'I0': I['I0_iom']['low_active|age+0']}, F0_HALL)['I'] * r99))
R = pd.DataFrame(rows)
# one-at-a-time parameter sensitivity (+/- 1 SD of Table 1) for waste increase and share change
oat = []
for k, (m, s) in TABLE1.items():
    for sgn in (-1, 1):
        p = {**NOMINAL, k: NOMINAL[k] + sgn * s} if k != 'gF' else {**NOMINAL, 'gF': 3.6 + sgn * s}
        r = summarize(f'{k} {"+" if sgn > 0 else "-"}1 SD', intake(pts['nchs'], YRS, p, F0_HALL)['I'])
        oat.append({'param': k, 'dir': sgn, 'value': p[k], 'increase_pct': r['increase_pct'], 'change_pp': r['change_pp'], 'waste_2003': r['waste_2003'], 'frac_2003': r['frac_2003']})
dump({'grid': R.round(3).to_dict('records'), 'oat': pd.DataFrame(oat).round(3).to_dict('records'), 'r99': r99, 'self_report_I0': sr}, 'robustness.json')
R.round(2).to_csv(f'{RES}/robustness.csv', index=False)
pd.set_option('display.width', 250); print(R.drop(columns='note').round(1).to_string()); print(pd.DataFrame(oat).round(1).to_string())
