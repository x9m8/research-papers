"""Deforestation embodied in EU27 imports of cattle hides and leather (HS 4101, 4104, 4107) under different allocation rules.
E_t = sum_c RHE_ct * alpha_ct * D_ct / Hides_ct, D = DeDuCE cattle-pasture deforestation risk (5-yr amortized, meat + leather), Hides = FAOSTAT raw hides of cattle (t).
Economic alpha_ct = P_hide * w_hide / (P_hide * w_hide + P_beef * k * w_carcass); P from EU import unit values (EUR/kg; raw hides 4101 from all extra-EU origins;
beef 0201+0202 from the origin, else all extra-EU), w from FAOSTAT kg per animal, k = boneless yield of carcass (0.70; 0.60-0.80 sensitivity)."""
import json, numpy as np, pandas as pd
from common import RES
X = pd.read_csv(f'{RES}/panel.csv')
K = 0.70
def econ(df, k=K, beef='origin'):
    pb = df.p_beef.fillna(df.p_beef_world) if beef == 'origin' else (df.p_beef_fixedmix if beef == 'fixedmix' else df.p_beef_world)
    wh = df.hide_kg_head; wc = df.carcass_kg_head
    return (df.p_hide_raw * wh) / (df.p_hide_raw * wh + pb * k * wc)
X['alpha_econ'] = econ(X); X['alpha_econ_k60'] = econ(X, 0.60); X['alpha_econ_k80'] = econ(X, 0.80); X['alpha_econ_worldbeef'] = econ(X, beef='world'); X['alpha_econ_fixedmix'] = econ(X, beef='fixedmix')
X['alpha_mass'] = X.hide_kg_head / (X.hide_kg_head + X.carcass_kg_head)
X['ha_per_t_all'] = X.amort_cattle / X.hides_t           # deforestation per tonne raw hide if hides carried all of it
X['ha_per_t_all_unam'] = X.unamort_cattle / X.hides_t
S = {'By-product (SWD), 2.5%': 0.025, 'PEFCR, 3.5%': 0.035, 'DeDuCE / SWD co-product, 5%': 0.05, 'Mass (SWD), 8%': 0.08, 'Mass (Laroche et al.), 10%': 0.10}
P = X[X.year.between(2005, 2022) & X.ha_per_t_all.notna() & np.isfinite(X.ha_per_t_all)].copy()
for name, a in S.items(): P[name] = P.t_rhe * a * P.ha_per_t_all
P['Economic, price of the year'] = P.t_rhe * P.alpha_econ * P.ha_per_t_all
P['Mass, FAOSTAT weights'] = P.t_rhe * P.alpha_mass * P.ha_per_t_all
P['Economic, k = 0.60'] = P.t_rhe * P.alpha_econ_k60 * P.ha_per_t_all; P['Economic, k = 0.80'] = P.t_rhe * P.alpha_econ_k80 * P.ha_per_t_all
P['Economic, world beef price'] = P.t_rhe * P.alpha_econ_worldbeef * P.ha_per_t_all
P['Economic, fixed-mix beef price'] = P.t_rhe * P.alpha_econ_fixedmix * P.ha_per_t_all
P['DeDuCE 5%, unamortized'] = P.t_rhe * 0.05 * P.ha_per_t_all_unam
cols = list(S) + ['Economic, price of the year', 'Mass, FAOSTAT weights', 'Economic, k = 0.60', 'Economic, k = 0.80', 'Economic, world beef price', 'Economic, fixed-mix beef price', 'DeDuCE 5%, unamortized']
Y = P.groupby('year')[cols].sum(); Y.to_csv(f'{RES}/embodied_by_year.csv')
P.to_csv(f'{RES}/embodied_by_origin_year.csv', index=False)
cov = X[X.year.between(2005, 2022)].groupby('year').apply(lambda g: g.loc[g.ha_per_t_all.notna() & np.isfinite(g.ha_per_t_all), 't_rhe'].sum() / g.t_rhe.sum())
# economic alpha weighted by EU raw-hide-equivalent imports from deforestation origins
dorig = P[P.amort_cattle > 0]
aw = dorig.groupby('year').apply(lambda g: np.average(g.alpha_econ.dropna(), weights=g.loc[g.alpha_econ.notna(), 't_rhe']) if g.alpha_econ.notna().any() else np.nan)
bra = X[X.iso3 == 'BRA'].set_index('year')[['alpha_econ', 'alpha_mass', 'p_beef', 'p_hide_raw', 'hide_kg_head', 'carcass_kg_head', 'amort_cattle', 'hides_t', 'ha_per_t_all', 't_rhe']]
pry = X[X.iso3 == 'PRY'].set_index('year')[['alpha_econ', 'p_beef', 'ha_per_t_all', 't_rhe']]
pr = X.groupby('year')[['p_hide_raw', 'p_beef_world']].first(); pr['ratio'] = pr.p_hide_raw / pr.p_beef_world
base = Y.loc[2015:2020].mean()
ext = pd.read_csv(f'{RES}/extra_eu_total_rhe.csv', index_col=0).t_rhe_extra_eu_total
cov_ext = X[X.year.between(2005, 2022)].groupby('year').apply(lambda g: g.loc[g.ha_per_t_all.notna() & np.isfinite(g.ha_per_t_all), 't_rhe'].sum()) / ext.loc[2005:2022]
awf = dorig.groupby('year').apply(lambda g: np.average(g.alpha_econ_fixedmix.dropna(), weights=g.loc[g.alpha_econ_fixedmix.notna(), 't_rhe']) if g.alpha_econ_fixedmix.notna().any() else np.nan)
mass_w = dorig.groupby('year').apply(lambda g: np.average(g.alpha_mass.dropna(), weights=g.loc[g.alpha_mass.notna(), 't_rhe']))
excluded = X[X.year.between(2015, 2020) & ~(X.ha_per_t_all.notna() & np.isfinite(X.ha_per_t_all))].groupby('iso3').t_rhe.sum().sort_values(ascending=False).head(10)
# SWD monetisation: implied EUR per ha from Annex II (sum of benefits / sum of hectares)
eur_per_ha = (978468 + 1956936) * 1000 / (19504 + 39005)
cost = 16741.51 * 1000
out = dict(coverage_share_of_eu_imports=cov.round(3).to_dict(), coverage_share_of_extra_eu_total=cov_ext.round(3).to_dict(), extra_eu_total_rhe={int(k): round(v) for k, v in ext.items()},
           alpha_weighted_fixedmix={int(k): round(v, 4) for k, v in awf.items()}, alpha_mass_weighted={int(k): round(v, 4) for k, v in mass_w.items()}, excluded_2015_2020_t_rhe=excluded.round(0).to_dict(),
           price_beef_fixedmix={int(k): round(v, 3) for k, v in X.groupby('year').p_beef_fixedmix.first().dropna().items()}, mean_2015_2020=base.round(0).to_dict(),
           mean_2018_2020=Y.loc[2018:2020].mean().round(0).to_dict(), y2022=Y.loc[2022].round(0).to_dict(),
           brazil_alpha={int(k): round(v, 4) for k, v in bra.alpha_econ.items() if not np.isnan(v)},
           brazil_share_2015_2020=float(P[P.year.between(2015, 2020) & (P.iso3 == 'BRA')]['DeDuCE / SWD co-product, 5%'].sum() / P[P.year.between(2015, 2020)]['DeDuCE / SWD co-product, 5%'].sum()),
           paraguay_share_2015_2020=float(P[P.year.between(2015, 2020) & (P.iso3 == 'PRY')]['DeDuCE / SWD co-product, 5%'].sum() / P[P.year.between(2015, 2020)]['DeDuCE / SWD co-product, 5%'].sum()),
           alpha_weighted={int(k): round(v, 4) for k, v in aw.items()},
           price_ratio={int(k): round(v, 4) for k, v in pr.ratio.items()}, price_hide={int(k): round(v, 3) for k, v in pr.p_hide_raw.items()}, price_beef={int(k): round(v, 3) for k, v in pr.p_beef_world.items()},
           eur_per_ha_swd=eur_per_ha, swd_cost=cost,
           benefit_cost_2015_2020={k: float(v * eur_per_ha / cost) for k, v in base.items()},
           benefit_cost_2022={k: float(v * eur_per_ha / cost) for k, v in Y.loc[2022].items()},
           breakeven_alpha_2015_2020=float(0.05 * cost / (base['DeDuCE / SWD co-product, 5%'] * eur_per_ha)))
json.dump(out, open(f'{RES}/analysis.json', 'w'), indent=1, default=float)
pd.set_option('display.width', 250)
print(Y.round(0).to_string()); print(json.dumps({k: out[k] for k in ['mean_2015_2020', 'brazil_share_2015_2020', 'paraguay_share_2015_2020', 'eur_per_ha_swd', 'breakeven_alpha_2015_2020']}, indent=1))
print(pd.Series(out['alpha_weighted']).round(4).to_string()); print(bra.round(4).to_string()); print(cov.round(3).to_string())
