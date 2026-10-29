"""Category-level diet models (TFP-style): y_c = grams/day of WWEIA category c (composite nutrients and price of what eligible adults eat in it).
Bounds 0 <= y_c <= max(P95 (or P99) of individual intake including non-eaters, current amount). Alcohol and plain water (tap, bottled) excluded.
 closest: minimise sum ((y_c - t_c) / t_c)^2 (QP), t_c = (1 - r) x current amount; closest_l1: sum |y_c - t_c| / t_c (LP); cheapest: minimise cost.
 Constraints from model.nutrient_rows at energy (1 - r) x current energy."""
import json, numpy as np, pandas as pd, cvxpy as cp
from scipy.optimize import linprog
from common import *
from model import nutrient_rows
C0 = pd.read_csv(f'{RES}/categories.csv')
DROP = {7502, 7504, 7506, 7702, 7704}
def setup(sex, bound='p95'):
    C = C0[(C0.sex == sex) & ~C0.cat.isin(DROP)].reset_index(drop=True)
    C['ub'] = np.maximum(C[bound], C.t); return C
def qp_closest(A, b, e, kcal, t, ub, extra=None):
    """min sum ((y - t) / t)^2 s.t. A y <= b, e y = kcal, 0 <= y <= ub (squared relative deviation; smoother than L1)."""
    y = cp.Variable(len(t)); cons = [A @ y <= b, e @ y == kcal, y >= 0, y <= ub]
    if extra is not None: cons += extra(y)
    pr = cp.Problem(cp.Minimize(cp.sum_squares(cp.multiply(1 / t, y - t))), cons)
    try: pr.solve(solver=cp.CLARABEL)
    except Exception: return None, pr
    if pr.status not in ('optimal', 'optimal_inaccurate'): return None, pr
    return np.maximum(y.value, 0), pr
def run(sex, r, prot_gkg=0.8, objective='closest', ub_mult=1.0, cost_cap=None, bound='p95', **kw):
    C = setup(sex, bound); t = C.t.values * (1 - r); n = len(C)
    kcal = float(t @ C['Energy (kcal)'].values / 100); price = C.price_100g.values / 100
    A, b, nm, e = nutrient_rows(C, sex, kcal, prot_gkg, **kw)
    ub = np.maximum(C.ub.values * ub_mult, t)
    unmet = [nm[k] for k in range(len(b)) if A[k] @ t > b[k] + 1e-6]
    if objective == 'closest':
        y, pr = qp_closest(A, b, e, kcal, t, ub)
        if y is not None:
            out = dict(sex=sex, r=r, prot_gkg=prot_gkg, objective=objective, kcal=kcal, cost_scaled=float(t @ price), scaled_unmet=unmet, feasible=True, **kw)
            out.update(cost=float(y @ price), grams=float(y.sum()), grams_scaled=float(t.sum()), share_changed=float(np.abs(y - t).sum() / 2 / t.sum()),
                       binding={nm[k]: float(pr.constraints[0].dual_value[k]) for k in range(len(b)) if abs(pr.constraints[0].dual_value[k]) > 1e-6}, n_at_ub=int(np.sum(y >= ub - 1e-6)))
            out['_y'] = y; out['_t'] = t; out['_C'] = C; return out
        y = None
    elif objective == 'closest_l1':
        c = np.concatenate([np.zeros(n), 1 / t, 1 / t]); Z = np.zeros((len(b), 2 * n))
        Aub = np.hstack([A, Z]); bub = b.copy()
        if cost_cap is not None: Aub = np.vstack([Aub, np.concatenate([price, np.zeros(2 * n)])]); bub = np.append(bub, cost_cap)
        Aeq = np.vstack([np.hstack([np.eye(n), -np.eye(n), np.eye(n)]), np.concatenate([e, np.zeros(2 * n)])]); beq = np.append(t, kcal)
        bounds = [(0, u) for u in ub] + [(0, None)] * (2 * n)
        res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=bounds, method='highs')
        y = res.x[:n] if res.status == 0 else None
    else:
        res = linprog(price, A_ub=A, b_ub=b, A_eq=e[None, :], b_eq=[kcal], bounds=[(0, u) for u in ub], method='highs'); y = res.x if res.status == 0 else None
    out = dict(sex=sex, r=r, prot_gkg=prot_gkg, objective=objective, kcal=kcal, cost_scaled=float(t @ price), scaled_unmet=unmet, feasible=y is not None, **kw)
    if y is None: return out
    du = -res.ineqlin.marginals[:len(b)]
    out.update(cost=float(y @ price), grams=float(y.sum()), grams_scaled=float(t.sum()), share_changed=float(np.abs(y - t).sum() / 2 / t.sum()),
               binding={nm[k]: float(du[k]) for k in range(len(b)) if abs(du[k]) > 1e-9}, n_at_ub=int(np.sum(y >= ub - 1e-6)))
    out['_y'] = y; out['_t'] = t; out['_C'] = C
    return out
if __name__ == '__main__':  # quick check
    for s in 'FM':
        for r in (0, 0.16, 0.24, 0.35, 0.39):
            for pg in (0.8, 1.2):
                for ob in ('closest', 'cheapest'):
                    o = run(s, r, pg, ob)
                    print(s, r, pg, ob[:5], round(o['kcal']), round(o['cost_scaled'], 2), o['feasible'], round(o.get('cost', 0), 2), round(o.get('share_changed', 0), 2), len(o['scaled_unmet']), [k[4:16] for k in o.get('binding', {})][:7])

def elastic(sex, r, prot_gkg=0.8, ub_mult=1.0, objective='closest', bound='p95', **kw):
    """Smallest total relative shortfall against the nutrient minima achievable within the bounds (each minimum may be missed by s_k >= 0,
    penalised by s_k / requirement_k); maxima, AMDR and energy are kept hard. Returns the % of each requirement met and the cost of that diet
    (cost minimised among diets with the smallest total shortfall)."""
    C = setup(sex, bound); t = C.t.values * (1 - r); n = len(C); kcal = float(t @ C['Energy (kcal)'].values / 100); price = C.price_100g.values / 100
    A, b, nm, e = nutrient_rows(C, sex, kcal, prot_gkg, **kw); ub = np.maximum(C.ub.values * ub_mult, t)
    mins = [k for k in range(len(b)) if nm[k].startswith('min ') and not nm[k].startswith('min protein 10') and '%' not in nm[k]]
    m = len(mins); S = np.zeros((len(b), m))
    for j, k in enumerate(mins): S[k, j] = -1.0                      # -a x <= -req  ->  -a x - s <= -req
    req = np.array([-b[k] for k in mins])
    Aub = np.hstack([A, S]); c1 = np.concatenate([np.zeros(n), 1 / req])
    bounds = [(0, u) for u in ub] + [(0, None)] * m
    Aeq = np.hstack([e[None, :], np.zeros((1, m))])
    r1 = linprog(c1, A_ub=Aub, b_ub=b, A_eq=Aeq, b_eq=[kcal], bounds=bounds, method='highs')
    if r1.status != 0: return dict(sex=sex, r=r, feasible=False)
    best = r1.fun
    if objective == 'cheapest':
        r2 = linprog(np.concatenate([price, np.zeros(m)]), A_ub=np.vstack([Aub, c1[None, :]]), b_ub=np.append(b, best + 1e-6), A_eq=Aeq, b_eq=[kcal], bounds=bounds, method='highs')
        x = r2.x[:n]; s = r2.x[n:]
    else:   # closest (squared relative deviation) to the scaled diet among diets with the smallest total shortfall
        yv = cp.Variable(n); sv = cp.Variable(m)
        cons = [Aub @ cp.hstack([yv, sv]) <= b, e @ yv == kcal, yv >= 0, yv <= ub, sv >= 0, c1[n:] @ sv <= best * (1 + 1e-6) + 1e-9]
        pr = cp.Problem(cp.Minimize(cp.sum_squares(cp.multiply(1 / t, yv - t))), cons); pr.solve(solver=cp.CLARABEL)
        if pr.status in ('optimal', 'optimal_inaccurate'):
            x = np.maximum(yv.value, 0); s = np.maximum(sv.value, 0)
            met = {nm[k][4:]: float(100 * (1 - s[j] / req[j])) for j, k in enumerate(mins)}
            return dict(sex=sex, r=r, prot_gkg=prot_gkg, ub_mult=ub_mult, feasible=True, objective=objective, kcal=kcal, total_rel_shortfall=float(best), cost=float(x @ price),
                        short={k: round(v, 1) for k, v in met.items() if v < 99.95}, share_changed=float(np.abs(x - t).sum() / 2 / t.sum()), _y=x, _t=t, _C=C, **kw)
        # fall back to L1 closeness: variables [x, s, d+, d-]
        Z = np.zeros
        A2 = np.vstack([np.hstack([Aub, Z((len(b), 2 * n))]), np.concatenate([c1, Z(2 * n)])[None, :]])
        Aeq2 = np.vstack([np.hstack([e[None, :], Z((1, m + 2 * n))]), np.hstack([np.eye(n), Z((n, m)), -np.eye(n), np.eye(n)])])
        r2 = linprog(np.concatenate([Z(n + m), 1 / t, 1 / t]), A_ub=A2, b_ub=np.append(b, best + 1e-6), A_eq=Aeq2, b_eq=np.concatenate([[kcal], t]),
                     bounds=bounds + [(0, None)] * (2 * n), method='highs')
        x = r2.x[:n]; s = r2.x[n:n + m]
    met = {nm[k][4:]: float(100 * (1 - s[j] / req[j])) for j, k in enumerate(mins)}
    return dict(sex=sex, r=r, prot_gkg=prot_gkg, ub_mult=ub_mult, feasible=True, objective=objective, kcal=kcal, total_rel_shortfall=float(best), cost=float(x @ price),
                short={k: round(v, 1) for k, v in met.items() if v < 99.95}, share_changed=float(np.abs(x - t).sum() / 2 / t.sum()), _y=x, _t=t, _C=C, **kw)
def max_r(sex, prot_gkg=0.8, ub_mult=1.0, feas=None, **kw):
    feas = feas or (lambda r: run(sex, r, prot_gkg, 'cheapest', ub_mult, **kw)['feasible'])
    lo, hi = 0.0, 0.6
    if not feas(0.0): return None
    for _ in range(18):
        mid = (lo + hi) / 2
        if feas(mid): lo = mid
        else: hi = mid
    return lo

def max_nutrient(sex, r, col, prot_gkg=0.8, bound='p95', **kw):
    """Highest intake of one nutrient (as % of its RDA) achievable with every other requirement met (vitamins D and E both dropped as constraints)."""
    C = setup(sex, bound); t = C.t.values * (1 - r); kcal = float(t @ C['Energy (kcal)'].values / 100)
    A, b, nm, e = nutrient_rows(C, sex, kcal, prot_gkg, vitd=False, vite=False, **kw); ub = np.maximum(C.ub.values, t)
    res = linprog(-C[col].values / 100, A_ub=A, b_ub=b, A_eq=e[None, :], b_eq=[kcal], bounds=[(0, u) for u in ub], method='highs')
    if res.status != 0: return None
    return float(-res.fun / MIN[col][0 if sex == 'M' else 1] * 100)
