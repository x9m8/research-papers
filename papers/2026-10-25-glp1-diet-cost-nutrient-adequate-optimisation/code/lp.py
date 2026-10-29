"""Least-cost nutritionally adequate diets by energy level (linear programming, scipy HiGHS).
Decision variable x_j = grams/day of food j. Minimise sum price_j * x_j subject to energy = E, RDA/AI minima, UL/CDRR maxima,
AMDR (protein 10-35%, fat 20-35%, carbohydrate 45-65%, linoleic 5-10%, ALA 0.6-1.2%), saturated fat < 10% energy, fibre >= 14 g/1000 kcal,
a per-food cap (150 g; 300 g for beverages and milks) and a cap per WWEIA group (first two digits of the category; 400 g, 600 g for beverage groups).
The AMDR upper bounds for linoleic acid and ALA are dropped by default because below about 1,530 kcal (men) they conflict with the absolute AIs."""
import json, sys, numpy as np, pandas as pd
from scipy.optimize import linprog
from common import *
D = pd.read_csv(f'{RES}/foods_priced.csv')
D['cat'] = D['WWEIA Category number'].astype(int)
E_ = 'Energy (kcal)'

def solve(sex, kcal, prot_gkg=0.8, excl=EXCL_MAIN, cap=150, bev_cap=300, fibre='per1000', vitd=True, amdr_prot_max=0.35, mass_cap=None, foods=None, ret=False, pufa_max=False, group_cap=400, bev_group_cap=600):
    F = D[~D.cat.isin(excl)].reset_index(drop=True) if foods is None else foods
    A = F.iloc[:, :0].copy(); per_g = lambda col: F[col].fillna(0).values / 100.0
    c = F.price_100g_2026.values / 100.0
    Aub, bub, names = [], [], []
    def ge(v, b, nm): Aub.append(-v); bub.append(-b); names.append('min ' + nm)
    def le(v, b, nm): Aub.append(v); bub.append(b); names.append('max ' + nm)
    i = 0 if sex == 'M' else 1
    for col, vals in MIN.items():
        if col.startswith('Vitamin D') and not vitd: continue
        ge(per_g(col), vals[i], col)
    for col, v in MAX.items(): le(per_g(col), v, col)
    e = per_g(E_); prot = per_g('Protein (g)'); fat = per_g('Total Fat (g)'); cho = per_g('Carbohydrate (g)')
    ge(prot, prot_gkg * REFWT[sex], 'protein g/kg')
    ge(4 * prot, 0.10 * kcal, 'protein 10%'); le(4 * prot, amdr_prot_max * kcal, 'protein 35%')
    ge(9 * fat, 0.20 * kcal, 'fat 20%'); le(9 * fat, 0.35 * kcal, 'fat 35%')
    ge(4 * cho, 0.45 * kcal, 'carb 45%'); le(4 * cho, 0.65 * kcal, 'carb 65%')
    le(9 * per_g('Fatty acids, total saturated (g)'), 0.10 * kcal, 'sat fat 10%')
    la = per_g('18:2\n(g)'); ala = per_g('18:3\n(g)')
    ge(9 * la, 0.05 * kcal, 'linoleic 5%'); ge(9 * ala, 0.006 * kcal, 'ALA 0.6%')
    if pufa_max: le(9 * la, 0.10 * kcal, 'linoleic 10%'); le(9 * ala, 0.012 * kcal, 'ALA 1.2%')
    fib = per_g('Fiber, total dietary (g)')
    ge(fib, FIBRE_PER_1000 * kcal / 1000 if fibre == 'per1000' else FIBRE_AI[sex], 'fibre')
    if mass_cap: le(np.ones(len(F)), mass_cap, 'food mass')
    if group_cap:
        grp = F.cat // 100
        for gv in sorted(grp.unique()):
            le((grp == gv).values.astype(float), bev_group_cap if gv in BEV_GROUPS else group_cap, f'group {gv}')
    ub = np.where(F.cat.isin(BEVERAGE), bev_cap, cap)
    r = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=e[None, :], b_eq=[kcal], bounds=list(zip(np.zeros(len(F)), ub)), method='highs')
    if r.status != 0: return dict(sex=sex, kcal=kcal, prot_gkg=prot_gkg, feasible=False)
    x = r.x; sel = x > 0.5
    out = dict(sex=sex, kcal=kcal, prot_gkg=prot_gkg, feasible=True, cost_day=float(r.fun), n_foods=int(sel.sum()), mass_g=float(x.sum()),
               protein_g=float(prot @ x), protein_pct=float(400 * (prot @ x) / kcal))
    # binding constraints: shadow prices (marginal cost of tightening by 1 unit)
    duals = -r.ineqlin.marginals
    out['binding'] = {nm: float(dv) for nm, dv in zip(names, duals) if abs(dv) > 1e-9}
    if ret:
        out['foods'] = F.loc[sel, ['Food code', 'Main food description', 'WWEIA Category description', 'price_100g_2026']].assign(grams=x[sel]).sort_values('grams', ascending=False)
    return out
