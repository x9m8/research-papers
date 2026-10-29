"""Nutrient constraint builder shared by all models, and the least-cost diet from any foods (the floor), chosen from all priced FNDDS foods with per-food and per-group caps.
(The food-level closest() below is an exploratory L1 variant not used in the paper.)
Constraints (adults 31-50): RDA/AI minima, UL and sodium CDRR maxima, AMDR for protein, fat and carbohydrate, saturated fat < 10% of energy,
linoleic >= 5% and ALA >= 0.6% of energy, fibre >= 14 g/1,000 kcal, energy fixed, protein >= target g/kg of reference weight."""
import json, numpy as np, pandas as pd
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack, vstack, identity
from common import *
B = pd.read_csv(f'{RES}/basket.csv'); D = pd.read_csv(f'{RES}/foods_priced.csv')
ALC = {7502, 7504, 7506}
def nutrient_rows(F, sex, kcal, prot_gkg, vitd=True, vite=True, age='31-50', fibre='per1000'):
    i = 0 if sex == 'M' else 1; pg = lambda col: F[col].fillna(0).values / 100.0
    A, b, nm = [], [], []
    def ge(v, x, n): A.append(-v); b.append(-x); nm.append('min ' + n)
    def le(v, x, n): A.append(v); b.append(x); nm.append('max ' + n)
    mins = dict(MIN)
    maxs = dict(MAX)
    if age == '51-70':
        mins.update({'Vitamin B-6 (mg)': (1.7, 1.5), 'Calcium (mg)': (1000, 1200), '18:2\n(g)': (14, 11), 'Iron\n(mg)': (8, 8)})
        maxs['Calcium (mg)'] = 2000
    for col, v in mins.items():
        if (col.startswith('Vitamin D') and not vitd) or (col.startswith('Vitamin E') and not vite): continue
        ge(pg(col), v[i], col)
    for col, v in maxs.items(): le(pg(col), v, col)
    pr, fat, cho = pg('Protein (g)'), pg('Total Fat (g)'), pg('Carbohydrate (g)')
    ge(pr, prot_gkg * REFWT[sex], 'protein target'); ge(4 * pr, 0.10 * kcal, 'protein 10%'); le(4 * pr, 0.35 * kcal, 'protein 35%')
    ge(9 * fat, 0.20 * kcal, 'fat 20%'); le(9 * fat, 0.35 * kcal, 'fat 35%'); ge(4 * cho, 0.45 * kcal, 'carb 45%'); le(4 * cho, 0.65 * kcal, 'carb 65%')
    le(9 * pg('Fatty acids, total saturated (g)'), 0.10 * kcal, 'sat fat 10%')
    ge(9 * pg('18:2\n(g)'), 0.05 * kcal, 'linoleic 5%'); ge(9 * pg('18:3\n(g)'), 0.006 * kcal, 'ALA 0.6%')
    if fibre == 'per1000': ge(pg('Fiber, total dietary (g)'), FIBRE_PER_1000 * kcal / 1000, 'fibre')
    else: ge(pg('Fiber, total dietary (g)'), (FIBRE_AI[sex] if age == '31-50' else {'M': 30, 'F': 21}[sex]), 'fibre')
    return np.array(A), np.array(b), nm, pg('Energy (kcal)')
def closest(sex, r, prot_gkg=0.8, **kw):
    F = B[(B[f'x0_{sex}'] > 0) & B.price_100g_2026.notna() & ~B['WWEIA Category number'].isin(ALC | {9999})].reset_index(drop=True)
    t = F[f'x0_{sex}'].values * (1 - r); kcal0 = float(t @ (F['Energy (kcal)'].values / 100)); n = len(F)
    A, b, nm, e = nutrient_rows(F, sex, kcal0, prot_gkg, **kw)
    # variables [x, dplus, dminus]; x - t = dplus - dminus
    c = np.concatenate([np.zeros(n), 1 / t, 1 / t])
    Aub = hstack([csr_matrix(A), csr_matrix((len(b), 2 * n))]); I = identity(n, format='csr')
    Aeq = vstack([hstack([I, -I, I]), hstack([csr_matrix(e[None, :]), csr_matrix((1, 2 * n))])])
    beq = np.concatenate([t, [kcal0]])
    res = linprog(c, A_ub=Aub, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * (3 * n), method='highs')
    base = dict(sex=sex, r=r, prot_gkg=prot_gkg, kcal=kcal0, cost_scaled=float(t @ F.price_100g_2026.values / 100), **{k: v for k, v in kw.items()})
    # adequacy of the scaled basket itself
    viol = [nm[k] for k in range(len(b)) if A[k] @ t > b[k] + 1e-6]; base['scaled_unmet'] = viol
    if res.status != 0: return dict(base, feasible=False)
    x = res.x[:n]
    du = -res.ineqlin.marginals
    return dict(base, feasible=True, cost=float(x @ F.price_100g_2026.values / 100), grams_moved=float(np.abs(x - t).sum() / 2), grams=float(t.sum()),
                share_changed=float(np.abs(x - t).sum() / 2 / t.sum()), binding={nm[k]: float(du[k]) for k in range(len(b)) if abs(du[k]) > 1e-9},
                _x=x, _F=F, _t=t)
def leastcost(sex, kcal, prot_gkg=0.8, cap=150, bev_cap=300, group_cap=400, bev_group_cap=600, **kw):
    F = D[~D['WWEIA Category number'].isin(EXCL_MAIN)].reset_index(drop=True); n = len(F)
    A, b, nm, e = nutrient_rows(F, sex, kcal, prot_gkg, **kw)
    grp = (F['WWEIA Category number'] // 100).values; G = []; gb = []
    for gv in np.unique(grp): G.append((grp == gv).astype(float)); gb.append(bev_group_cap if gv in BEV_GROUPS else group_cap)
    ub = np.where(F['WWEIA Category number'].isin(BEVERAGE), bev_cap, cap)
    res = linprog(F.price_100g_2026.values / 100, A_ub=np.vstack([A, np.array(G)]), b_ub=np.concatenate([b, gb]), A_eq=e[None, :], b_eq=[kcal],
                  bounds=list(zip(np.zeros(n), ub)), method='highs')
    if res.status != 0: return dict(sex=sex, kcal=kcal, prot_gkg=prot_gkg, feasible=False)
    return dict(sex=sex, kcal=kcal, prot_gkg=prot_gkg, feasible=True, cost=float(res.fun), n_foods=int((res.x > 0.5).sum()), _x=res.x, _F=F)
if __name__ == '__main__':  # exploratory only
    for s in 'FM':
        for r in (0, 0.16, 0.24, 0.35, 0.39):
            for pg in (0.8, 1.2):
                o = closest(s, r, pg)
                print(s, r, pg, round(o['kcal']), round(o['cost_scaled'], 2), o['feasible'], round(o.get('cost', 0), 2), round(o.get('share_changed', 0), 3), len(o['scaled_unmet']), list(o.get('binding', {}))[:6])
