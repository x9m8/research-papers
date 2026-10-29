"""Origin tracing of raw-hide equivalents (RHE) to EU27 final demand, per year.

Stage-wise model (this paper): four physical trade matrices (raw hides, tanned/crust, finished leather, articles), each solved with
the re-export algorithm of Kastner et al. (2011). The origin-specific 'production' of stage s+1 in country c is c's domestic use of
stage s (supply minus exports), with the origin mix of c's stage-s supply. Stage 1 production is FAOSTAT hide output (cattle + buffalo).
Domestic use of articles in the EU27 is taken as EU final consumption. Exports that exceed a country's supply at a stage are scaled down
to supply (recorded).

Pooled model (replication of Laroche et al. 2024, 01_calculations.R): all stages summed into one RHE trade matrix, traced once with
hide production; apparent consumption = production + imports - exports, origins in proportion to supply.

Exporter attribution (the companion paper, paper 8): EU27 direct imports by exporting country, in RHE, times the exporter's
own deforestation per tonne of hide."""
import json, numpy as np, pandas as pd
from common import DER, RES, EU, STAGE, EXTRA3, YEARS, CF_SETS, CORE_CF, cf_set, RULES, BR_YIELDS

T = pd.read_csv(f'{DER}/trade.csv.gz', dtype={'i': str, 'j': str, 'k': str})
H = pd.read_csv(f'{DER}/hides.csv', dtype={'region': str})
BA = pd.read_csv(f'{DER}/hides_brazil_alt.csv')
CHN = '156'

def matrices(t, cf, extra3=False, bovine_goods=1.0):
    d = T[T.t == t].copy()
    st = dict(STAGE)
    if extra3: st.update({k: 3 for k in EXTRA3})
    d = d[d.k.isin(st)]
    d['s'] = d.k.map(st); d['rhe'] = d.q * d.k.map(cf)
    d.loc[d.s == 4, 'rhe'] *= bovine_goods
    return d.groupby(['s', 'j', 'i']).rhe.sum()   # j importer, i exporter

def kastner(Tm, Pm, balance='clip'):
    """Tm[c, e]: imports of c from e. Pm[c, o]: production in c of origin o. Returns supply-by-origin R, supply x, exports, T, gap.
    Where a country's exports exceed its supply (production + imports), balance='clip' scales its exports down to its supply;
    balance='topup' adds the missing supply to the country, with the origin mix of its existing supply (its own origin if it has none)."""
    imp = Tm.sum(1); x = Pm.sum(1) + imp; exp = Tm.sum(0)
    over = exp > x + 1e-9
    clipped = float((exp - x)[over].sum())
    if over.any() and balance == 'topup':
        Pm = Pm.copy(); N = len(x)
        for _ in range(50):
            inv = np.where(x > 0, 1 / np.where(x > 0, x, 1), 0)
            R = np.linalg.solve(np.eye(N) - Tm * inv[None, :], Pm)
            over = exp > x * (1 + 1e-9) + 1e-6
            if not over.any(): break
            for c in np.nonzero(over)[0]:
                gap = exp[c] - x[c]
                if x[c] > 0: Pm[c] += gap * R[c] / x[c]
                else: Pm[c, c] += gap
            x = Pm.sum(1) + imp
        return R, x, exp, Tm, clipped
    for _ in range(100):   # scaling one exporter's sales can push an importer below its own exports, so repeat until none exceeds supply
        if not over.any(): break
        sc = np.ones_like(exp); sc[over] = np.where(exp[over] > 0, x[over] / exp[over], 0); Tm = Tm * sc[None, :]
        imp = Tm.sum(1); x = Pm.sum(1) + imp; exp = Tm.sum(0)
        over = exp > x * (1 + 1e-12) + 1e-9
    inv = np.where(x > 0, 1 / np.where(x > 0, x, 1), 0)
    A = Tm * inv[None, :]
    R = np.linalg.solve(np.eye(len(x)) - A, Pm)
    return R, x, exp, Tm, clipped

def run_year(t, cfname='Commission SWD', china=1.0, extra3=False, bovine_goods=1.0, balance='clip', brazil_yield=0, routes=False):
    cf = cf_set(cfname)
    M = matrices(t, cf, extra3, bovine_goods)
    h = H[H.t == t].set_index('region').hides.copy()
    if CHN in h: h[CHN] *= china
    if brazil_yield: h['76'] = BA[(BA.t == t) & (BA.brazil_yield == brazil_yield)].hides.iloc[0]
    regs = sorted(set(M.index.get_level_values(1)) | set(M.index.get_level_values(2)) | set(h.index))
    ix = {r: n for n, r in enumerate(regs)}; N = len(regs); e = ix[EU]
    def tm(s):
        m = np.zeros((N, N))
        if s in M.index.get_level_values(0):
            ms = M.loc[s]
            m[[ix[a] for a in ms.index.get_level_values(0)], [ix[b] for b in ms.index.get_level_values(1)]] = ms.values
        return m
    Ts = {s: tm(s) for s in (1, 2, 3, 4)}
    P = np.zeros((N, N)); hv = h.reindex(regs).fillna(0).values; P[np.arange(N), np.arange(N)] = hv
    out = dict(t=t, cf=cfname, china=china, extra3=extra3, bovine=bovine_goods, balance=balance, brazil_yield=brazil_yield, regions=regs)
    # ---- stage-wise ----
    route = {('EU production', EU): P[e].copy()}   # composition of EU supply by entry route
    stages = {}
    for s in (1, 2, 3, 4):
        R, x, exp, Tm, clipped = kastner(Ts[s], P, balance)
        mix = np.where(x[:, None] > 0, R / np.where(x[:, None] > 0, x[:, None], 1), 0)
        d = np.clip(x - exp, 0, None)
        if routes:
            for j in np.nonzero(Tm[e])[0]:
                route[(s, regs[j])] = route.get((s, regs[j]), 0) + Tm[e, j] * mix[j]
            tot = sum(v.sum() for v in route.values()); fac = d[e] / tot if tot > 0 else 0
            stages[s] = {k: v * fac for k, v in route.items()}     # composition of EU domestic use at stage s
            route = {k: v * fac for k, v in route.items()}
        out[f's{s}'] = dict(x=x, exp=exp, d=d, clipped=clipped, eu_supply=R[e].copy(), eu_use=d[e] * mix[e], eu_exports=exp[e] * mix[e],
                            eu_imports_by_exporter=Tm[e].copy(), eu_imports_traced=Tm[e] @ mix, world_supply=x.sum(), world_exp=exp.sum())
        P = d[:, None] * mix
    out['stagewise_eu'] = out['s4']['eu_use']
    if routes: out['routes'] = stages
    # ---- pooled (Laroche) ----
    Tall = Ts[1] + Ts[2] + Ts[3] + Ts[4]
    Pp = np.zeros((N, N)); Pp[np.arange(N), np.arange(N)] = hv
    imp = Tall.sum(1); x = hv + imp; exp = Tall.sum(0)
    inv = np.where(x > 0, 1 / np.where(x > 0, x, 1), 0)
    R = np.linalg.solve(np.eye(N) - Tall * inv[None, :], Pp)
    ac = x - exp
    out['pooled_eu'] = ac[e] * inv[e] * R[e]
    out['pooled_neg'] = float(-(ac[ac < 0]).sum())
    # ---- exporter attribution: direct EU imports by exporter ----
    out['exporter_hides_leather'] = Ts[1][e] + Ts[2][e] + Ts[3][e]
    out['exporter_goods'] = Ts[4][e]
    return out

def frame(vec, regs, **kw):
    return pd.DataFrame(dict(origin=regs, rhe=vec, **kw)).query('rhe != 0')

if __name__ == "__main__":
    rows, bal, rts = [], [], []
    scen = [dict(cfname=c) for c in CF_SETS] + [dict(cfname=c, balance='topup') for c in CF_SETS] + [dict(cfname=CORE_CF, china=0.5), dict(cfname=CORE_CF, china=0.0),
            dict(cfname=CORE_CF, extra3=True), dict(cfname=CORE_CF, bovine_goods=0.75)] + [dict(cfname=CORE_CF, brazil_yield=y) for y in BR_YIELDS] + [dict(cfname='Commission SWD', brazil_yield=30)]
    for t in YEARS + [2024]:
        for sc in scen:
            core = sc == dict(cfname=CORE_CF)
            o = run_year(t, routes=core, **sc)
            lab = dict(t=t, cf=o['cf'], china=o['china'], extra3=o['extra3'], bovine=o['bovine'], balance=o['balance'], brazil_yield=o['brazil_yield'])
            regs = o['regions']
            rows += [frame(o['stagewise_eu'], regs, method='Stage-wise tracing', **lab), frame(o['pooled_eu'], regs, method='Pooled tracing (Laroche)', **lab),
                     frame(o['exporter_hides_leather'], regs, method='Exporter: hides and leather', **lab), frame(o['exporter_goods'], regs, method='Exporter: articles', **lab)]
            for s in (1, 2, 3, 4):
                S = o[f's{s}']
                bal.append(dict(**lab, stage=s, world_supply=S['world_supply'], world_exports=S['world_exp'], clipped=S['clipped'],
                                eu_supply=S['eu_supply'].sum(), eu_use=S['eu_use'].sum(), eu_exports=S['eu_exports'].sum(),
                                eu_imports=S['eu_imports_by_exporter'].sum(), world_use=S['d'].sum(), pooled_negative=o['pooled_neg']))
                for oo, v in zip(regs, S['eu_exports']):
                    if v: rts.append(dict(**lab, kind='EU exports', stage=s, entry='', origin=oo, rhe=v))
                for oo, v in zip(regs, S['eu_use']):
                    if v: rts.append(dict(**lab, kind='EU domestic use', stage=s, entry='', origin=oo, rhe=v))
                for oo, v in zip(regs, S['eu_imports_traced']):
                    if v: rts.append(dict(**lab, kind='EU imports traced', stage=s, entry='', origin=oo, rhe=v))
            hv_eu = H[(H.t == t) & (H.region == EU)].hides.sum() * 1.0
            rts.append(dict(**lab, kind='EU hide production', stage=0, entry='', origin=EU, rhe=hv_eu))
            if core:
                for (es, ec), vec in o['routes'][4].items():
                    for oo, v in zip(regs, vec):
                        if v: rts.append(dict(**lab, kind='EU final use by entry route', stage=es, entry=ec, origin=oo, rhe=v))
        print(t, flush=True)
    pd.concat(rows).to_csv(f'{RES}/eu_rhe_by_origin.csv.gz', index=False)
    pd.DataFrame(bal).to_csv(f'{RES}/stage_balance.csv', index=False)
    pd.DataFrame(rts).to_csv(f'{RES}/eu_routes.csv.gz', index=False)
