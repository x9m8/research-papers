"""Assemble model inputs: mean adult body-weight series, initial fat mass F0, IOM baseline intake, FAO food supply.
Writes data/derived/bw_points.csv, data/derived/fa.csv and results/inputs.json."""
import numpy as np, pandas as pd
from common import *

fao = load_fao(); A, E = load_nhanes(); O = load_ogden(); D = load_digitized()
out = {}

# ---------- FAO food supply ----------
fbsh = fao['FBSH']['2901'].rename('fbsh'); fbs = fao['FBS']['2901'].rename('fbs')
pop = pd.concat([fao['FBSH']['pop_1000'], fao['FBS']['pop_1000'].loc[2014:]]).rename('pop_1000')
fa = pd.concat([fbsh, fbs, pop, fao['FBSH']['2924'].rename('alc_fbsh'), fao['FBS']['2924'].rename('alc_fbs')], axis=1)
ov = (fbs - fbsh).dropna()
out['fao_overlap_2010_2013'] = {'years': list(ov.index), 'fbs_minus_fbsh': ov.round(2).tolist(), 'mean': round(float(ov.mean()), 2)}
fa['spliced'] = fa['fbsh']
fa.loc[2014:, 'spliced'] = fa.loc[2014:, 'fbs'] - ov.mean()     # new-methodology series shifted to the old level
fa.to_csv(f'{DER}/fa.csv')
out['fa'] = {str(y): {'fbsh': fa.loc[y, 'fbsh'], 'fbs': fa.loc[y, 'fbs'], 'pop_1000': fa.loc[y, 'pop_1000']} for y in (1974, 2000, 2003, 2010, 2013, 2019, 2022, 2023)}

# ---------- body weight points ----------
pts = []
dg = D[D.panel == 'A']
for _, r in dg.iterrows(): pts.append(('hall_digitized', r.year, r.value, 'Hall et al. (2009) Fig. 1A, digitized'))

def comb(m, w, pw=P_W): return (1 - pw) * m + pw * w
og = O[O.ages == '20-74']
pos = {'NHANES I': 1974.0, 'NHANES II': 1978.5, 'NHANES III': 1991.0}
for s, t in pos.items():
    m = og[(og.survey == s) & (og.sex == 1)].iloc[0]; w = og[(og.survey == s) & (og.sex == 2)].iloc[0]
    pts.append(('nchs', t, comb(m.wt_kg, w.wt_kg), f'{s}, Ogden et al. (2004) Table 7, 20-74 y, pregnant excluded'))
    pts.append(('nchs_20p', t, comb(m.wt_kg, w.wt_kg), f'{s}, Ogden et al. (2004) Table 7, 20-74 y (no 75+ sampled)'))
o3 = O[(O.ages == '20+') & (O.survey == 'NHANES III')]
mid = {'1999-2000': 1999.5, '2001-2002': 2001.5, '2003-2004': 2003.5, '2005-2006': 2005.5, '2007-2008': 2007.5, '2009-2010': 2009.5,
       '2011-2012': 2011.5, '2013-2014': 2013.5, '2015-2016': 2015.5, '2017-2018': 2017.5, '2021-2023': 2022.5}
for cyc, t in mid.items():
    a = A[(A.cycle == cyc)]
    g = lambda sex, ages, pr: a[(a.sex == sex) & (a.ages == ages) & (a.pregnant == pr)].iloc[0]
    m, w = g(1, '2074', 'excl'), g(2, '2074', 'excl')
    pts.append(('nchs', t, comb(m.wt_kg, w.wt_kg), f'NHANES {cyc} microdata, 20-74 y, pregnant excluded'))
    m2, w2 = g(1, '20p', 'incl'), g(2, '20p', 'incl')
    pts.append(('nchs_20p', t, comb(m2.wt_kg, w2.wt_kg), f'NHANES {cyc} microdata, 20+ y, all'))
    pw = w.sumw / (w.sumw + m.sumw)
    pts.append(('nchs_wshare', t, comb(m.wt_kg, w.wt_kg, pw), f'NHANES {cyc}, 20-74, survey-weighted female share {pw:.3f}'))
# NHANES III as 20+ in the 20p variant
for i, p in enumerate(pts):
    if p[0] == 'nchs_20p' and p[3].startswith('NHANES III'):
        m = o3[o3.sex == 1].iloc[0]; w = o3[o3.sex == 2].iloc[0]
        pts[i] = ('nchs_20p', 1991.0, comb(m.wt_kg, w.wt_kg), 'NHANES III, Ogden et al. (2004) Table 7, 20+ y, pregnant excluded')
for s, t in pos.items():   # female-share variant uses the fixed share before 1999 (no weights published)
    m = og[(og.survey == s) & (og.sex == 1)].iloc[0]; w = og[(og.survey == s) & (og.sex == 2)].iloc[0]
    pts.append(('nchs_wshare', t, comb(m.wt_kg, w.wt_kg), f'{s}, fixed share 0.525'))
P = pd.DataFrame(pts, columns=['series', 't', 'bw', 'source']).sort_values(['series', 't'])
P.to_csv(f'{DER}/bw_points.csv', index=False)
out['bw_points'] = {s: [[round(t, 2), round(b, 3)] for t, b in zip(g.t, g.bw)] for s, g in P.groupby('series')}
# check: continuous 1999-2002 vs Ogden 1999-2002 published (20-74, pregnant excluded)
chk = {}
for sex in (1, 2):
    sub = A[(A.cycle.isin(['1999-2000', '2001-2002'])) & (A.sex == sex) & (A.ages == '2074') & (A.pregnant == 'excl')]
    chk[sex] = {'micro_pooled_wt': round(float((sub.wt_kg * sub.sumw).sum() / sub.sumw.sum()), 2),
                'ogden_wt': float(og[(og.survey == 'NHANES 1999-2002') & (og.sex == sex)].wt_kg.iloc[0]),
                'micro_pooled_bmi': round(float((sub.bmi * sub.sumw).sum() / sub.sumw.sum()), 2),
                'ogden_bmi': float(og[(og.survey == 'NHANES 1999-2002') & (og.sex == sex)].bmi.iloc[0])}
out['check_microdata_vs_ogden_1999_2002'] = chk

# ---------- initial fat mass F0 ----------
# Exact for continuous cycles; for NHANES I (1971-74, published means only) E[BMI*BW] and E[BMI^2*BW] are approximated by
# E[BMI]E[BW] and E[BMI]^2 E[BW] times the ratios observed in NHANES 1999-2000 (same age range, pregnant excluded).
ratios = {}
for sex in (1, 2):
    r = A[(A.cycle == '1999-2000') & (A.sex == sex) & (A.ages == '2074') & (A.pregnant == 'excl')].iloc[0]
    ratios[sex] = (r.bmi_x_wt / (r.bmi * r.wt_kg), r.bmi2_x_wt / (r.bmi ** 2 * r.wt_kg))
F = {}
for sex in (1, 2):
    n1 = og[(og.survey == 'NHANES I') & (og.sex == sex)].iloc[0]
    F[sex] = jackson_fat(sex, n1.wt_kg, n1.bmi * n1.wt_kg * ratios[sex][0], n1.bmi ** 2 * n1.wt_kg * ratios[sex][1])
F0 = (1 - P_W) * F[1] + P_W * F[2]
Fnr = {sex: jackson_fat(sex, og[(og.survey == 'NHANES I') & (og.sex == sex)].iloc[0].wt_kg,
                       og[(og.survey == 'NHANES I') & (og.sex == sex)].iloc[0].bmi * og[(og.survey == 'NHANES I') & (og.sex == sex)].iloc[0].wt_kg,
                       og[(og.survey == 'NHANES I') & (og.sex == sex)].iloc[0].bmi ** 2 * og[(og.survey == 'NHANES I') & (og.sex == sex)].iloc[0].wt_kg) for sex in (1, 2)}
Fcont = {}
for cyc in ('1999-2000', '2003-2004', '2021-2023'):
    v = {}
    for sex in (1, 2):
        r = A[(A.cycle == cyc) & (A.sex == sex) & (A.ages == '2074') & (A.pregnant == 'excl')].iloc[0]
        v[sex] = jackson_fat(sex, r.wt_kg, r.bmi_x_wt, r.bmi2_x_wt)
    Fcont[cyc] = {'men': round(v[1], 2), 'women': round(v[2], 2), 'pooled_pw0.525': round((1 - P_W) * v[1] + P_W * v[2], 2)}
out['F0'] = {'hall': F0_HALL, 'nhanes1_calibrated': round(F0, 3), 'men': round(F[1], 2), 'women': round(F[2], 2),
             'nhanes1_no_dispersion_adjustment': round((1 - P_W) * Fnr[1] + P_W * Fnr[2], 3),
             'ratios_1999': {str(k): [round(x, 4) for x in v] for k, v in ratios.items()}, 'continuous_cycles': Fcont,
             'alpha_hall': round(NOMINAL['C'] / F0_HALL, 4), 'alpha_here': round(NOMINAL['C'] / F0, 4)}

# ---------- coefficients of eq. 14 ----------
cd, cs = coefs(NOMINAL, F0_HALL); cdT, csT = coefs({**NOMINAL, 'gF': 3.6}, F0_HALL)
out['coefficients'] = {'C_dyn_nominal': round(cd, 1), 'C_static_nominal': round(cs, 2), 'C_dyn_gF3.6': round(cdT, 1), 'C_static_gF3.6': round(csT, 2),
                       'published': {'C_dyn': 9100, 'C_static': 22}}

# ---------- IOM baseline intake for the 1971-74 adult population ----------
def eer_adult(sex, age, wt, htm, pa=1.0):
    return 662 - 9.53 * age + pa * (15.91 * wt + 539.6 * htm) if sex == 1 else 354 - 6.91 * age + pa * (9.36 * wt + 726 * htm)
ages99 = {sex: A[(A.cycle == '1999-2000') & (A.sex == sex) & (A.ages == '2074') & (A.pregnant == 'excl')].iloc[0].age for sex in (1, 2)}
I0 = {}
for lab, pa in (('sedentary', (1.0, 1.0)), ('low_active', (1.11, 1.12))):
    for dage in (-3, 0, 3):
        v = []
        for sex in (1, 2):
            n1 = og[(og.survey == 'NHANES I') & (og.sex == sex)].iloc[0]
            v.append(eer_adult(sex, ages99[sex] + dage, n1.wt_kg, n1.ht_cm / 100, pa[sex - 1]))
        I0[f'{lab}|age{dage:+d}'] = round((1 - P_W) * v[0] + P_W * v[1], 1)
out['I0_iom'] = I0; out['I0_ages_used'] = {str(k): round(v, 2) for k, v in ages99.items()}
dump(out, 'inputs.json'); print(json.dumps({k: out[k] for k in ('fao_overlap_2010_2013', 'F0', 'coefficients', 'I0_iom', 'check_microdata_vs_ogden_1999_2002')}, indent=1))
print(P.to_string())
