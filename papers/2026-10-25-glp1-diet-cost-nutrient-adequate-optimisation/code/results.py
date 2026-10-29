"""All results for the paper -> results/results.json, results/diets_by_category.csv.
Main specification: WWEIA category composites, each category <= max(P95 of individual intake incl. non-eaters, current amount); all nutrient
constraints except vitamins D and E; protein >= 0.8 g/kg reference weight; DRIs for ages 31-50; fibre 14 g/1,000 kcal; closest diet = QP."""
import json, numpy as np, pandas as pd
from common import *
from catmodel import run, elastic, max_r, setup, max_nutrient
from within import run_food
import model
RS = [0.0, 0.16, 0.24, 0.35, 0.39]
NODE = dict(vitd=False, vite=False)
DCOL, ECOL = 'Vitamin D (D2 + D3) (mcg)', 'Vitamin E (alpha-tocopherol) (mg)'
def realloc(o):
    C = o['_C']; k = C['Energy (kcal)'].values / 100; return float(np.abs((o['_y'] - o['_t']) * k).sum() / 2 / (o['_t'] * k).sum())
def adequate(s, r, pg=0.8, **kw):
    """Closest adequate diet, or the best achievable (smallest total shortfall, then closest) if none exists."""
    o = run(s, r, pg, 'closest', **NODE, **kw)
    if o['feasible']: return o, dict(feasible=True, cost=o['cost'], realloc=realloc(o))
    el = elastic(s, r, pg, **NODE, **{k: v for k, v in kw.items() if k != 'objective'})
    return el, dict(feasible=False, cost=el['cost'], realloc=realloc(el), short=el['short'])
if __name__ == '__main__':
    out = dict(tfp_day={s: v / 7 for s, v in TFP_WEEK_JUNE2026.items()}, grid={}, frontier={}, sens={}, de={}, p95_zero={})
    rows = []
    for s in 'FM':
        C = setup(s); out['p95_zero'][s] = dict(n_cat=len(C), n_zero=int((C.p95 == 0).sum()))
        for r in RS:
            for pg in (0.8, 1.2):
                key = f'{s}|{r}|{pg}'
                cl, a = adequate(s, r, pg); ch = run(s, r, pg, 'cheapest', **NODE)
                g = dict(kcal=cl['kcal'], cost_scaled=float(cl['_t'] @ cl['_C'].price_100g.values / 100),
                         scaled_unmet=[u[4:] for u in run(s, r, pg, 'cheapest', **NODE)['scaled_unmet']], adequate=a,
                         cheapest=dict(feasible=ch['feasible'], cost=ch.get('cost'), realloc=realloc(ch) if ch['feasible'] else None))
                fl = model.leastcost(s, cl['kcal'], pg, **NODE); g['floor'] = dict(cost=fl.get('cost'), n_foods=fl.get('n_foods'))
                if pg == 0.8:
                    g['p99'] = adequate(s, r, pg, bound='p99')[1]
                    fw = run_food(s, r, pg, cap_mult=5, **NODE); g['food5_cheapest'] = fw.get('cost')
                    for lab, y in (('scaled', cl['_t']), ('adequate', cl['_y'])):
                        rows += [dict(sex=s, r=r, diet=lab, cat=c, desc=d, grams=float(v), kcal=float(v * k / 100)) for c, d, v, k in zip(cl['_C'].cat, cl['_C'].desc, y, cl['_C']['Energy (kcal)'])]
                out['grid'][key] = g
                print(key, round(g['cost_scaled'], 2), {k: (round(v, 2) if isinstance(v, float) else v) for k, v in a.items()}, g.get('p99'), g.get('food5_cheapest'))
        # feasibility frontier (protein 0.8)
        for lab, kw in (('all', {}), ('no_D_E', NODE)):
            out['frontier'][f'{s}|cat_p95|{lab}'] = max_r(s, **kw)
            out['frontier'][f'{s}|cat_p99|{lab}'] = max_r(s, bound='p99', **kw)
            out['frontier'][f'{s}|food5|{lab}'] = max_r(s, feas=lambda r, kw=kw: run_food(s, r, cap_mult=5, **kw)['feasible'])
            out['frontier'][f'{s}|food_free|{lab}'] = max_r(s, feas=lambda r, kw=kw: run_food(s, r, **kw)['feasible'])
        out['frontier'][f'{s}|cat_p95|no_D_E|fibre_abs'] = max_r(s, fibre='abs', **NODE)
        # vitamins D and E: highest % of RDA achievable from food with every other requirement met
        for r in RS:
            out['de'][f'{s}|{r}'] = dict(D=max_nutrient(s, r, DCOL), E=max_nutrient(s, r, ECOL), D_p99=max_nutrient(s, r, DCOL, bound='p99'), E_p99=max_nutrient(s, r, ECOL, bound='p99'))
        # sensitivity at 24% and 35%
        for r in (0.24, 0.35):
            for lab, kw in (('l1', dict(objective='closest_l1')), ('fibre_abs', dict(fibre='abs')), ('age51', dict(age='51-70'))):
                if lab == 'l1':
                    o = run(s, r, 0.8, 'closest_l1', **NODE)
                    out['sens'][f'{s}|{r}|{lab}'] = dict(feasible=o['feasible'], cost=o.get('cost'))
                else:
                    out['sens'][f'{s}|{r}|{lab}'] = adequate(s, r, 0.8, **kw)[1]
    pd.DataFrame(rows).to_csv(f'{RES}/diets_by_category.csv', index=False)
    json.dump(out, open(f'{RES}/results.json', 'w'), indent=1, default=lambda o: None)
    print(json.dumps({k: out[k] for k in ('frontier', 'de', 'sens', 'p95_zero')}, indent=0))
