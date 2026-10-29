"""Embodied deforestation in EU27 leather consumption: stage-wise origin tracing vs pooled tracing vs exporter attribution."""
import json, numpy as np, pandas as pd
from common import DER, RES, RAW, EU, YEARS, CF_SETS, CORE_CF, RULES, ALL_RULES, CORE_RULE

names = json.load(open(f'{DER}/regions.json'))['name']
I = pd.read_csv(f'{DER}/intensity.csv', dtype={'region': str})
d = pd.read_csv(f'{RES}/eu_rhe_by_origin.csv.gz', dtype={'origin': str})
d = d[d.t.isin(YEARS)].merge(I[['region', 't', 'ha_per_t', 'ha_per_t_v20', 'alpha_econ', 'alpha_mass']].rename(columns={'region': 'origin'}), on=['origin', 't'], how='left')
for c in ['ha_per_t', 'ha_per_t_v20']: d[c] = d[c].fillna(0)
# Brazil hide-yield sensitivity: Brazil's deforestation per tonne uses the assumed hide output
BA = pd.read_csv(f'{DER}/hides_brazil_alt.csv')
DB = I[I.region == '76'].set_index('t')
for y in BA.brazil_yield.unique():
    hb = BA[BA.brazil_yield == y].set_index('t').hides
    m = (d.brazil_yield == y) & (d.origin == '76')
    d.loc[m, 'ha_per_t'] = d.loc[m, 't'].map(DB.D / hb).values
    d.loc[m, 'ha_per_t_v20'] = d.loc[m, 't'].map(DB.D20 / hb).values
def alpha(df, rule):
    if rule in RULES: return RULES[rule]
    return df.alpha_econ if rule.startswith('Economic') else df.alpha_mass
for r in ALL_RULES: d[r] = d.rhe * alpha(d, r) * d.ha_per_t
d['5% v2.0'] = d.rhe * 0.05 * d.ha_per_t_v20
dBR = d[d.brazil_yield > 0].copy(); d = d[d.brazil_yield == 0].copy()
base = (d.china == 1) & (~d.extra3) & (d.bovine == 1)
core = base & (d.cf == CORE_CF) & (d.balance == 'clip')
M = ['Stage-wise tracing', 'Pooled tracing (Laroche)', 'Exporter: hides and leather', 'Exporter: articles']
d.loc[d.method.isin(M[2:]), 'method2'] = 'Exporter: all direct imports'
ex_all = d[d.method.isin(M[2:])].assign(method='Exporter: all direct imports')
d = pd.concat([d.drop(columns='method2'), ex_all.drop(columns='method2')]); core = (d.china == 1) & (~d.extra3) & (d.bovine == 1) & (d.cf == CORE_CF) & (d.balance == 'clip')
M = M + ['Exporter: all direct imports']
keys = ['t', 'cf', 'balance', 'china', 'extra3', 'bovine', 'method']   # Brazil-yield runs are summarised separately
Y = d.groupby(keys)[['rhe'] + ALL_RULES + ['5% v2.0']].sum().reset_index()
Y.to_csv(f'{RES}/eu_embodied_by_year.csv', index=False)
yc = Y[(Y.cf == CORE_CF) & (Y.balance == 'clip') & (Y.china == 1) & (~Y.extra3) & (Y.bovine == 1)]
series = yc.pivot(index='t', columns='method', values=CORE_RULE)
series_rhe = yc.pivot(index='t', columns='method', values='rhe')
def per(df, a, b, col=CORE_RULE): return df[df.t.between(a, b)].groupby([k for k in keys if k != 't'])[col].mean()
out = {}
out['series_ha_5pct'] = {m: {int(t): round(v) for t, v in series[m].items()} for m in M}
out['series_rhe_kt'] = {m: {int(t): round(v / 1e3, 1) for t, v in series_rhe[m].items()} for m in M}
for a, b in [(2015, 2020), (2018, 2020), (2005, 2009), (2021, 2023), (2005, 2023)]:
    s = yc[yc.t.between(a, b)].groupby('method')[ALL_RULES + ['rhe', '5% v2.0']].mean()
    out[f'mean_{a}_{b}'] = {m: s.loc[m].round(0).to_dict() for m in M}
s = out['mean_2015_2020']
out['ratio_stagewise_to_exporterHL_2015_2020'] = {r: s['Stage-wise tracing'][r] / s['Exporter: hides and leather'][r] for r in ALL_RULES}
out['ratio_stagewise_to_exporterAll_2015_2020'] = {r: s['Stage-wise tracing'][r] / s['Exporter: all direct imports'][r] for r in ALL_RULES}
out['ratio_pooled_to_stagewise_2015_2020'] = s['Pooled tracing (Laroche)'][CORE_RULE] / s['Stage-wise tracing'][CORE_RULE]
ann = series['Stage-wise tracing'] / series['Exporter: hides and leather']
out['ratio_stagewise_to_exporterHL_by_year'] = {int(k): round(v, 3) for k, v in ann.items()}
# trend in ratio
out['ratio_trend_slope_per_year'] = float(np.polyfit(ann.index, ann.values, 1)[0])
# factor sets and balancing, 2015-2020, 5%
g = Y[(Y.china == 1) & (~Y.extra3) & (Y.bovine == 1) & Y.t.between(2015, 2020)].groupby(['cf', 'balance', 'method'])[[CORE_RULE, 'rhe']].mean()
out['cf_grid_2015_2020'] = {f'{cf} | {bal}': {m: dict(ha=round(g.loc[(cf, bal, m), CORE_RULE]), rhe_kt=round(g.loc[(cf, bal, m), 'rhe'] / 1e3)) for m in M} for cf in CF_SETS for bal in ['clip', 'topup']}
rng = [out['cf_grid_2015_2020'][k]['Stage-wise tracing']['ha'] for k in out['cf_grid_2015_2020']]
rngx = [out['cf_grid_2015_2020'][k]['Exporter: hides and leather']['ha'] for k in out['cf_grid_2015_2020']]
out['stagewise_range_over_cf_balance_2015_2020'] = [min(rng), max(rng)]; out['exporterHL_range_over_cf_balance_2015_2020'] = [min(rngx), max(rngx)]
out['ratio_range_over_cf_balance_2015_2020'] = [min(a / b for a, b in zip(rng, rngx)), max(a / b for a, b in zip(rng, rngx))]
# scenarios
sc = Y[(Y.cf == CORE_CF) & (Y.balance == 'clip') & Y.t.between(2015, 2020) & (Y.method == 'Stage-wise tracing')].groupby(['china', 'extra3', 'bovine'])[[CORE_RULE, 'rhe']].mean()
out['scenarios_2015_2020'] = {f'china={a}, extra3={b}, bovine={c}': dict(ha=round(v[CORE_RULE]), rhe_kt=round(v['rhe'] / 1e3)) for (a, b, c), v in sc.iterrows()}
# origin shares 2015-2020 (core)
def shares(method, col):
    x = d[core & (d.method == method) & d.t.between(2015, 2020)].groupby('origin')[col].sum()
    return (x / x.sum()).sort_values(ascending=False)
out['origin_share_ha_2015_2020'] = {m: {names.get(k, k): round(v, 4) for k, v in shares(m, CORE_RULE).head(8).items()} for m in M}
out['origin_share_rhe_2015_2020'] = {m: {names.get(k, k): round(v, 4) for k, v in shares(m, 'rhe').head(8).items()} for m in M}
bo = d[core & d.t.between(2015, 2020)].groupby(['method', 'origin'])[[CORE_RULE, 'rhe']].sum().div(6)
out['brazil_paraguay_2015_2020'] = {m: {names[o]: dict(ha=round(bo.loc[(m, o), CORE_RULE]) if (m, o) in bo.index else 0, rhe_kt=round(bo.loc[(m, o), 'rhe'] / 1e3, 1) if (m, o) in bo.index else 0) for o in ['76', '600', '68', '32', '156', '699', EU]} for m in M}
# rule range, stage-wise vs exporter
out['rule_range_2015_2020'] = {m: [min(s[m][r] for r in ALL_RULES), max(s[m][r] for r in ALL_RULES)] for m in M}
# routes: EU final use by entry route, core
R = pd.read_csv(f'{RES}/eu_routes.csv.gz', dtype={'origin': str, 'entry': str})
R = R[R.t.isin(YEARS) & (R.cf == CORE_CF) & (R.balance == 'clip') & (R.china == 1) & (~R.extra3) & (R.bovine == 1) & (R.brazil_yield == 0)]
R['stage'] = R.stage.astype(str)
R = R.merge(I[['region', 't', 'ha_per_t']].rename(columns={'region': 'origin'}), on=['origin', 't'], how='left').fillna({'ha_per_t': 0})
R['ha'] = R.rhe * 0.05 * R.ha_per_t
fr = R[R.kind == 'EU final use by entry route'].copy()
fr['route'] = np.where(fr.entry == EU, 'EU hides', np.where(fr.entry == fr.origin, 'Direct from origin', 'Via third country'))
fr['entry_stage'] = fr.stage.map({'1': 'raw hides', '2': 'tanned/crust', '3': 'finished leather', '4': 'articles'}).fillna('EU hides')
rt = fr[fr.t.between(2015, 2020)]
def route_tab(sub):
    a = sub.groupby(['route', 'entry_stage'])[['rhe', 'ha']].sum().div(6)
    return {f'{i} | {j}': dict(rhe_kt=round(v.rhe / 1e3, 1), ha=round(v.ha)) for (i, j), v in a.iterrows()}
out['routes_all_2015_2020'] = route_tab(rt)
out['routes_brazil_2015_2020'] = route_tab(rt[rt.origin == '76'])
out['routes_paraguay_2015_2020'] = route_tab(rt[rt.origin == '600'])
bz = rt[rt.origin.isin(['76', '600'])]
out['brpy_indirect_share_rhe_2015_2020'] = float(bz[bz.route == 'Via third country'].rhe.sum() / bz.rhe.sum())
out['all_indirect_share_ha_2015_2020'] = float(rt[rt.route == 'Via third country'].ha.sum() / rt.ha.sum())
via = bz[bz.route == 'Via third country'].groupby('entry').rhe.sum().sort_values(ascending=False)
out['brpy_indirect_entry_countries_share'] = {names.get(k, k): round(v / via.sum(), 4) for k, v in via.head(8).items()}
viah = rt[rt.route == 'Via third country'].groupby('entry').ha.sum().sort_values(ascending=False)
out['indirect_ha_entry_countries_share'] = {names.get(k, k): round(v / viah.sum(), 4) for k, v in viah.head(8).items()}
byr = fr.groupby(['t', 'route']).ha.sum().unstack().fillna(0); byr.to_csv(f'{RES}/routes_ha_by_year.csv')
out['indirect_share_ha_by_year'] = {int(t): round(v, 3) for t, v in (byr['Via third country'] / byr.sum(1)).items()}
bzy = fr[fr.origin.isin(['76', '600'])].groupby(['t', 'route']).rhe.sum().unstack().fillna(0)
out['brpy_indirect_share_rhe_by_year'] = {int(t): round(v, 3) for t, v in (bzy['Via third country'] / bzy.sum(1)).items()}
fr.groupby(['t', 'route', 'entry_stage', 'entry'])[['rhe', 'ha']].sum().reset_index().to_csv(f'{RES}/routes_by_entry.csv', index=False)
# EU exports (offset) and EU use by stage, core
ex = R[R.kind == 'EU exports'].astype({'stage': int}).groupby(['t', 'stage'])[['rhe', 'ha']].sum().reset_index()
ex.to_csv(f'{RES}/eu_exports_by_stage.csv', index=False)
e1520 = ex[ex.t.between(2015, 2020)].groupby('stage')[['rhe', 'ha']].mean()
out['eu_exports_2015_2020'] = {int(s): dict(rhe_kt=round(v.rhe / 1e3), ha=round(v.ha)) for s, v in e1520.iterrows()}
exb = R[(R.kind == 'EU exports') & R.t.between(2015, 2020) & R.origin.isin(['76', '600'])].groupby('stage').rhe.sum() / 6
out['eu_exports_brpy_rhe_kt_2015_2020'] = {int(k): round(v / 1e3, 1) for k, v in exb.items()}
# bridge from exporter attribution (hides and leather) to stage-wise consumption, 2015-2020, 5%
def rsum(kind, stages):
    x = R[(R.kind == kind) & R.stage.isin([str(s) for s in stages]) & R.t.between(2015, 2020)]
    return x.ha.sum() / 6
A_ = s['Exporter: hides and leather'][CORE_RULE]
bridge = {'Exporter attribution, hides and leather': A_,
          'Re-attribution of hides and leather imports to cattle origin': rsum('EU imports traced', [1, 2, 3]) - A_,
          'Articles imported, traced to cattle origin': rsum('EU imports traced', [4]),
          'EU-produced hides': rsum('EU hide production', [0]),
          'Minus EU exports (all stages), traced': -rsum('EU exports', [1, 2, 3, 4])}
bridge['Sum'] = sum(bridge.values()); bridge['Stage-wise tracing (model)'] = s['Stage-wise tracing'][CORE_RULE]
out['bridge_2015_2020_ha'] = {k: round(v) for k, v in bridge.items()}
# mass-balance diagnostics
B = pd.read_csv(f'{RES}/stage_balance.csv')
B0 = B
B = B[(B.china == 1) & (~B.extra3) & (B.bovine == 1) & (B.brazil_yield == 0) & B.t.between(2015, 2020)]
gap = B.groupby(['cf', 'balance', 'stage'])[['clipped', 'world_exports']].mean()
out['gap_2015_2020_kt'] = {f'{cf} | stage {s}': dict(gap_kt=round(gap.loc[(cf, 'clip', s), 'clipped'] / 1e3), share_of_world_exports=round(gap.loc[(cf, 'clip', s), 'clipped'] / gap.loc[(cf, 'clip', s), 'world_exports'], 3)) for cf in CF_SETS for s in (1, 2, 3, 4)}
# Brazil yield sensitivity summary, 2015-2020, 5%
YB = dBR.groupby(['t', 'cf', 'brazil_yield', 'method'])[[CORE_RULE, '5% v2.0', 'rhe']].sum().reset_index()
YB = YB[YB.t.between(2015, 2020)].groupby(['cf', 'brazil_yield', 'method'])[[CORE_RULE, 'rhe']].mean()
brs = {}
for (cf_, y) in sorted({(a, b) for a, b, _ in YB.index}):
    sw = YB.loc[(cf_, y, 'Stage-wise tracing'), CORE_RULE]; ex_ = YB.loc[(cf_, y, 'Exporter: hides and leather'), CORE_RULE]
    xb = dBR[(dBR.cf == cf_) & (dBR.brazil_yield == y) & (dBR.method == 'Stage-wise tracing') & dBR.t.between(2015, 2020)]
    bsh = xb[xb.origin == '76'][CORE_RULE].sum() / xb[CORE_RULE].sum()
    gp = B0[(B0.cf == cf_) & (B0.brazil_yield == y) & (B0.balance == 'clip') & B0.t.between(2015, 2020)].groupby('stage')[['clipped', 'world_exports']].mean()
    brs[f'{cf_} | {y} kg'] = dict(stagewise_ha=round(sw), exporterHL_ha=round(ex_), ratio=round(sw / ex_, 3), brazil_share_stagewise=round(bsh, 4),
                                  gap_share_tanned=round(gp.loc[2, 'clipped'] / gp.loc[2, 'world_exports'], 4), gap_share_finished=round(gp.loc[3, 'clipped'] / gp.loc[3, 'world_exports'], 4))
out['brazil_yield_sensitivity_2015_2020'] = brs
BAy = BA[BA.t.between(2005, 2024)].drop_duplicates('t').set_index('t').faostat_yield
out['brazil_faostat_yield_kg_head'] = dict(min=round(BAy.min(), 1), max=round(BAy.max(), 1), by_year={int(k): round(v, 1) for k, v in BAy.items()})
Wf = pd.read_csv(f'{RAW}/faostat_qcl_cattle.csv')
Wf = Wf[(Wf.Item == 'Raw hides and skins of cattle') & (Wf.Element == 'Yield/Carcass Weight') & Wf.Year.between(2015, 2020)]
out['hide_yield_kg_head_2015_2020'] = {a_: [round(Wf[Wf.Area == a_].Value.min(), 1), round(Wf[Wf.Area == a_].Value.max(), 1)] for a_ in ['Brazil', 'United States of America', 'Argentina', 'Uruguay', 'China, mainland', 'Australia', 'Paraguay']}
# exporter attribution with the Commission factors and DeDuCE v2.0 (companion paper's data), 2015-2020, 5%
out['exporterHL_commission_factors_v20_2015_2020'] = round(Y[(Y.cf == 'Commission SWD') & (Y.balance == 'clip') & (Y.china == 1) & (~Y.extra3) & (Y.bovine == 1) & (Y.method == 'Exporter: hides and leather') & Y.t.between(2015, 2020)]['5% v2.0'].mean())
# India: deforestation per tonne uses buffalo hides only (FAOSTAT has no cattle-hide output for India)
ind = I[(I.region == '699') & I.t.between(2015, 2020)]
out['india_2015_2020'] = dict(D_ha=round(ind.D.mean()), hides_cattle_t=round(ind.hides_cattle.mean()), hides_buffalo_t=round(ind.hides_buffalo.mean()), ha_per_t=round(ind.ha_per_t.mean(), 4))
H = pd.read_csv(f'{DER}/hides.csv', dtype={'region': str})
out['world_hides_kt_2015_2020'] = round(H[H.t.between(2015, 2020)].groupby('t').hides.sum().mean() / 1e3)
out['eu_share_of_world_hides_rhe_2015_2020'] = float(s['Stage-wise tracing']['rhe'] * 1e3 / 1e3 / H[H.t.between(2015, 2020)].groupby('t').hides.sum().mean())
# Laroche published output (HS12, DeDuCE v1.0, 10%), for validation of the pooled replication
try:
    import pyreadr
    L = pyreadr.read_r(f'{DER}/../laroche/out_mean.rds')[None]
    le = L[(L['Consumer.Country'] == 5707) & (L['processing.level'] == 4)]
    ly = le.groupby('Year')[['primary.equivalents', 'deforestation.ha']].sum()
    out['laroche_published_level4'] = {int(k): dict(rhe_kt=round(v['primary.equivalents'] / 1e3), ha_10pct=round(v['deforestation.ha'])) for k, v in ly.iterrows()}
    out['laroche_published_level4_2018_2020'] = dict(rhe_kt=round(ly.loc[2018:2020, 'primary.equivalents'].mean() / 1e3), ha_10pct=round(ly.loc[2018:2020, 'deforestation.ha'].mean()))
    # origin shares (BACI codes) in their level-4 EU consumption, 2018-2020
    lo = le[le.Year.between(2018, 2020)].groupby('Producer.Country')['primary.equivalents'].sum()
    out['laroche_origin_share_2018_2020'] = {names.get(str(k), 'EU27' if k == 5707 else str(k)): round(v / lo.sum(), 3) for k, v in lo.sort_values(ascending=False).head(6).items()}
except Exception as ex_:
    out['laroche_error'] = str(ex_)
pooled1820 = yc[yc.t.between(2018, 2020) & (yc.method == 'Pooled tracing (Laroche)')][['rhe', 'Mass (Laroche et al.), 10%']].mean()
out['pooled_replication_2018_2020'] = dict(rhe_kt=round(pooled1820.rhe / 1e3), ha_10pct=round(pooled1820['Mass (Laroche et al.), 10%']))
json.dump(out, open(f'{RES}/analysis.json', 'w'), indent=1, default=float)
pd.set_option('display.width', 250)
print(series.round(0).to_string()); print(json.dumps({k: out[k] for k in ['mean_2015_2020', 'ratio_stagewise_to_exporterHL_2015_2020', 'stagewise_range_over_cf_balance_2015_2020', 'exporterHL_range_over_cf_balance_2015_2020',
      'ratio_range_over_cf_balance_2015_2020', 'scenarios_2015_2020', 'origin_share_ha_2015_2020', 'routes_brazil_2015_2020', 'brpy_indirect_share_rhe_2015_2020', 'brpy_indirect_entry_countries_share',
      'all_indirect_share_ha_2015_2020', 'indirect_ha_entry_countries_share', 'eu_exports_2015_2020', 'gap_2015_2020_kt', 'laroche_published_level4_2018_2020', 'pooled_replication_2018_2020', 'laroche_origin_share_2018_2020']}, indent=1, default=float))
# cross-check: BACI EU27 extra imports vs Eurostat Comext (paper 8 extract), tonnes, HS 4101/4104/4107
from common import RAW
Tq = pd.read_csv(f'{DER}/trade.csv.gz', dtype={'i': str, 'j': str, 'k': str})
bq = Tq[(Tq.j == EU) & Tq.k.str[:4].isin(['4101', '4104', '4107'])].assign(h4=lambda x: x.k.str[:4]).groupby(['t', 'h4']).q.sum()
c = pd.read_csv(f'{RAW}/x9p8-comext-eu27-4101-4104-4107.csv', dtype={'product': str, 'partner': str}, keep_default_na=False)
c['value'] = pd.to_numeric(c.value, errors='coerce')
cq = c[(c.partner == 'EXT_EU27_2020') & (c.indicator == 'QUANTITY_IN_100KG')].groupby(['year', 'product']).value.sum() / 10
cmp_ = pd.DataFrame({'baci_t': bq, 'comext_t': cq.rename_axis(['t', 'h4'])}).dropna()
cmp_ = cmp_[cmp_.index.get_level_values(0).isin(YEARS)]
r = (cmp_.baci_t / cmp_.comext_t).groupby(level=1).agg(['median', 'min', 'max'])
out['baci_vs_comext_ratio'] = {k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in r.iterrows()}
json.dump(out, open(f'{RES}/analysis.json', 'w'), indent=1, default=float)
print(out['baci_vs_comext_ratio'])
# DeDuCE v2.1: leather share of pasture deforestation
dd = pd.read_csv(f'{RAW}/x9p14-deduce21-attrib-cattle.csv')
pv = dd.pivot_table(index=['ISO', 'Year'], columns='Commodity', values='Deforestation risk, amortized (ha)', aggfunc='sum').dropna()
pv = pv[(pv.sum(1) > 0)]; sh_ = pv['Leather'] / pv.sum(1)
out['deduce21_leather_share'] = dict(min=float(sh_.min()), max=float(sh_.max()), n=int(len(sh_)))
out['deduce21_cattle_ha'] = {int(k): round(v) for k, v in dd.groupby('Year')['Deforestation risk, amortized (ha)'].sum().items() if k >= 2005}
fq = pd.read_csv(f'{RAW}/faostat_qcl_hides.csv')
fq = fq[(fq.Element == 'Production') & fq['Item Code'].isin([919, 957]) & fq.Year.between(2005, 2024) & fq.Value.notna()]
out['faostat_flags_countries'] = fq[fq['Area Code'] < 300].Flag.fillna('official').value_counts().to_dict()
out['faostat_flags_eu27_aggregate'] = fq[fq['Area Code'] == 5707].Flag.fillna('official').value_counts().to_dict()
out['faostat_flags_all_records_incl_aggregates'] = fq.Flag.fillna('official').value_counts().to_dict()
json.dump(out, open(f'{RES}/analysis.json', 'w'), indent=1, default=float)
print(out['deduce21_leather_share'], out['faostat_flags_countries'], out['faostat_flags_eu27_aggregate'])
