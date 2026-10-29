"""Food-level alternative: choose among the foods eligible adults already eat (x0 > 0), each category total limited as in the category model,
each food optionally limited to k times its current mean; the mix within categories is free. Cheapest diet and feasibility."""
import numpy as np, pandas as pd
from scipy.optimize import linprog
from common import *
from model import nutrient_rows
from catmodel import setup
B = pd.read_csv(f'{RES}/basket.csv')
def run_food(sex, r, prot_gkg=0.8, cap_mult=None, bound='p95', **kw):
    C = setup(sex, bound)
    F = B[(B[f'x0_{sex}'] > 0) & B.price_100g_2026.notna() & B['WWEIA Category number'].isin(C.cat)].reset_index(drop=True)
    t = C.t.values * (1 - r); kcal = float(t @ C['Energy (kcal)'].values / 100)
    A, b, nm, e = nutrient_rows(F, sex, kcal, prot_gkg, **kw)
    cat = F['WWEIA Category number'].values; G = np.array([(cat == c).astype(float) for c in C.cat]); ub = np.maximum(C.ub.values, t)
    fub = [None] * len(F) if cap_mult is None else list(cap_mult * F[f'x0_{sex}'].values)
    res = linprog(F.price_100g_2026.values / 100, A_ub=np.vstack([A, G]), b_ub=np.concatenate([b, ub]), A_eq=e[None, :], b_eq=[kcal],
                  bounds=[(0, u) for u in fub], method='highs')
    if res.status != 0: return dict(feasible=False)
    x = res.x; return dict(feasible=True, cost=float(res.fun), n_foods=int((x > 0.5).sum()), _x=x, _F=F)
