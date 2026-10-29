"""Assemble inputs: cleaned BACI bilateral trade (EU27 as one region), FAOSTAT hide production, DeDuCE cattle deforestation,
allocation factors (paper 8's seven rules) and deforestation intensities per tonne of raw hide."""
import glob, json, numpy as np, pandas as pd
from common import RAW, DER, RES, EU, EU27_ISO2, STAGE, EXTRA3, YEARS

# ---------- BACI ----------
cc = pd.read_csv(f'{RAW}/baci/country-codes.csv', dtype={'country_iso2': str}, keep_default_na=False, encoding='latin-1')
cc['country_code'] = cc.country_code.astype(int)
eu_codes = set(cc.loc[cc.country_iso2.isin(EU27_ISO2), 'country_code']) - {58}   # 58 = Belgium-Luxembourg (pre-1999), absent here
name = dict(zip(cc.country_code.astype(str), cc.country_name)); name[EU] = 'EU27'
iso3 = dict(zip(cc.country_code.astype(str), cc.country_iso3)); iso3['490'] = 'TWN'; iso3[EU] = EU
keep = set(STAGE) | set(EXTRA3)
T = []
for f in sorted(glob.glob(f'{RAW}/baci/leather_*.csv')):
    d = pd.read_csv(f, dtype={'k': str}); d = d[d.k.isin(keep)]; T.append(d)
T = pd.concat(T, ignore_index=True)
n_rows = len(T); n_q_missing = int(T.q.isna().sum())
# quantity cleaning (as Laroche et al. 2024, threshold 20x the year-product median unit value); missing q imputed from value
T['uv'] = T.v / T.q
T['uv_med'] = T.groupby(['t', 'k']).uv.transform('median')
bad = T.q.isna() | (T.uv > 20 * T.uv_med) | (T.uv < T.uv_med / 20)
T['q_clean'] = np.where(bad, T.v / T.uv_med, T.q); T['q_imputed'] = bad
T['i'] = np.where(T.i.isin(eu_codes), EU, T.i.astype(str)); T['j'] = np.where(T.j.isin(eu_codes), EU, T.j.astype(str))
intra = T[(T.i == EU) & (T.j == EU)]
T = T[T.i != T.j].groupby(['t', 'i', 'j', 'k'], as_index=False).agg(v=('v', 'sum'), q=('q_clean', 'sum'), q_raw=('q', 'sum'))
T.to_csv(f'{DER}/trade.csv.gz', index=False)
qinfo = dict(rows=n_rows, q_missing=n_q_missing, q_replaced_or_imputed=int(bad.sum()), share_q_replaced=float(bad.mean()))

# ---------- FAOSTAT hide production (cattle 919 + buffalo 957), tonnes ----------
q = pd.read_csv(f'{RAW}/faostat_qcl_hides.csv', dtype={'Area Code (M49)': str})
q['m49'] = q['Area Code (M49)'].str.strip("'").astype(int)
P = q[(q.Element == 'Production') & q['Item Code'].isin([919, 957]) & q.Year.between(2005, 2024)].copy()
special = {250: 251, 380: 381, 578: 579, 356: 699, 756: 757, 840: 842, 158: 490, 630: 842}
codes = set(cc.country_code)
P['region'] = None
P.loc[P['Area Code'] == 5707, 'region'] = EU
ok = (P['Area Code'] < 300) & ~P['Area Code'].isin([351])   # countries only; 351 = China aggregate
eu_m49 = set(cc.loc[cc.country_iso2.isin(EU27_ISO2), 'country_code']) | {250, 380}
m = ok & ~P.m49.isin(eu_m49)
P.loc[m, 'region'] = P.loc[m, 'm49'].map(lambda c: str(special.get(c, c)) if special.get(c, c) in codes else None)
unmatched = P[m & P.region.isna()].groupby('Area').Value.sum().sort_values(ascending=False)
P = P[P.region.notna()]
flags = P.Flag.fillna('official').value_counts().to_dict()
H = P.groupby(['region', 'Year', 'Item Code']).Value.sum().unstack(fill_value=0).rename(columns={919: 'hides_cattle', 957: 'hides_buffalo'}).reset_index().rename(columns={'Year': 't'})
H['hides'] = H.hides_cattle + H.hides_buffalo
H.to_csv(f'{DER}/hides.csv', index=False)
# Brazil hide-yield sensitivity: cattle hides = FAOSTAT head slaughtered x assumed yield (kg/head), plus FAOSTAT buffalo hides
from common import BR_YIELDS
fc = pd.read_csv(f'{RAW}/faostat_qcl_cattle.csv')
sl = fc[(fc.Area == 'Brazil') & (fc.Item == 'Raw hides and skins of cattle') & (fc.Element == 'Producing Animals/Slaughtered')].set_index('Year').Value
hb = H[H.region == '76'].set_index('t')
BA = pd.concat([pd.DataFrame(dict(t=hb.index, brazil_yield=y, hides=sl.reindex(hb.index).values * y / 1000 + hb.hides_buffalo.values,
                                  faostat_yield=hb.hides_cattle.values / sl.reindex(hb.index).values * 1000)) for y in BR_YIELDS])
BA.to_csv(f'{DER}/hides_brazil_alt.csv', index=False)

# ---------- DeDuCE cattle-pasture deforestation (meat + leather), amortised, ha ----------
def deduce(path):
    d = pd.read_csv(path)
    d = d.groupby(['ISO', 'Year'])['Deforestation risk, amortized (ha)'].sum().reset_index()
    i3 = {v: k for k, v in iso3.items() if k not in ('736', '891', '58')}
    eu3 = set(cc.loc[cc.country_iso2.isin(EU27_ISO2), 'country_iso3'])
    def reg(r):
        if r.ISO in eu3: return EU
        if r.ISO in ('SDN', 'SSD', 'SDN and SSD') and r.Year <= 2011: return '736'
        if r.ISO == 'SDN and SSD': return '729'
        if r.ISO in ('GUF', 'GLP', 'MTQ', 'REU'): return EU   # French outermost regions are part of the EU
        if r.ISO == 'PRI': return '842'                       # Puerto Rico is reported with the USA in BACI
        if r.ISO in ('SRB', 'MNE') and r.Year <= 2005: return '891'
        return i3.get(r.ISO)
    d['region'] = d.apply(reg, axis=1)
    miss = d[d.region.isna()].groupby('ISO')['Deforestation risk, amortized (ha)'].sum()
    d = d.dropna(subset=['region']).groupby(['region', 'Year'])['Deforestation risk, amortized (ha)'].sum().reset_index()
    return d.rename(columns={'Year': 't', 'Deforestation risk, amortized (ha)': 'D'}), miss
D21, miss21 = deduce(f'{RAW}/x9p14-deduce21-attrib-cattle.csv')
D20, miss20 = deduce(f'{RAW}/x9p8-deduce-attrib-cattle.csv')
# Sudan: FAOSTAT 'Sudan (former)' covers 2005-2011 and maps to 736; from 2012 Sudan = 729.

# ---------- allocation factors (paper 8 rules) ----------
f = pd.read_csv(f'{RAW}/faostat_qcl_cattle.csv', dtype={'Area Code (M49)': str})
f['m49'] = f['Area Code (M49)'].str.strip("'").astype(int)
key = {('Raw hides and skins of cattle', 'Yield/Carcass Weight'): 'hide_kg_head', ('Meat of cattle with the bone, fresh or chilled', 'Yield/Carcass Weight'): 'carcass_kg_head'}
f['var'] = [key.get((a, b)) for a, b in zip(f.Item, f.Element)]
f = f[f['var'].notna()]
f['region'] = None
f.loc[f['Area Code'] == 5707, 'region'] = EU
mm = (f['Area Code'] < 300) & ~f['Area Code'].isin([351]) & ~f.m49.isin(eu_m49)
f.loc[mm, 'region'] = f.loc[mm, 'm49'].map(lambda c: str(special.get(c, c)) if special.get(c, c) in codes else None)
W = f[f.region.notna()].pivot_table(index=['region', 'Year'], columns='var', values='Value', aggfunc='first').reset_index().rename(columns={'Year': 't'})
# prices: EU import unit values (paper 8): raw hides 4101 all extra-EU origins; beef 0201+0202 by origin (>=100 t), else all extra-EU
h = pd.read_csv(f'{RAW}/x9p8-comext-eu27-hs6-beef-origins-1.csv', dtype={'product': str, 'partner': str}, keep_default_na=False)
h['value'] = pd.to_numeric(h.value, errors='coerce'); h['hs4'] = h['product'].str.zfill(4).str[:4]
Hh = h.pivot_table(index=['partner', 'year', 'hs4'], columns='indicator', values='value', aggfunc='sum').reset_index()
Hh['kg'] = Hh.QUANTITY_IN_100KG * 100; Hh['uv'] = Hh.VALUE_IN_EUROS / Hh.kg
p_hide = Hh[(Hh.partner == 'EXT_EU27_2020') & (Hh.hs4 == '4101')].set_index('year').uv
beef = Hh[Hh.hs4.isin(['0201', '0202'])].groupby(['partner', 'year'])[['VALUE_IN_EUROS', 'kg']].sum().reset_index()
beef['p'] = beef.VALUE_IN_EUROS / beef.kg
p_beef_world = beef[beef.partner == 'EXT_EU27_2020'].set_index('year').p
beef = beef[(beef.partner != 'EXT_EU27_2020') & (beef.kg >= 100_000)]
a2_to_code = {r.country_iso2: str(r.country_code) for r in cc.itertuples() if r.country_iso2 and r.country_code not in (58, 736, 891)}
beef['region'] = beef.partner.map(a2_to_code)
pb = beef.dropna(subset=['region']).set_index(['region', 'year']).p
K = 0.70
A = W.copy()
A['p_hide'] = A.t.map(p_hide); A['p_beef'] = [pb.get((r, t), np.nan) for r, t in zip(A.region, A.t)]
A['p_beef'] = A.p_beef.fillna(A.t.map(p_beef_world))
A['alpha_econ'] = A.p_hide * A.hide_kg_head / (A.p_hide * A.hide_kg_head + A.p_beef * K * A.carcass_kg_head)
A['alpha_mass'] = A.hide_kg_head / (A.hide_kg_head + A.carcass_kg_head)

# ---------- intensities: ha of cattle deforestation per tonne raw hide if the hide carried all of it ----------
I = H.merge(D21, on=['region', 't'], how='left').merge(D20.rename(columns={'D': 'D20'}), on=['region', 't'], how='left')
I = I.merge(A[['region', 't', 'alpha_econ', 'alpha_mass']], on=['region', 't'], how='left')
I[['D', 'D20']] = I[['D', 'D20']].fillna(0)
I['ha_per_t'] = np.where(I.hides > 0, I.D / I.hides, 0.0); I['ha_per_t_v20'] = np.where(I.hides > 0, I.D20 / I.hides, 0.0)
I['ha_per_t_cattleonly'] = np.where(I.hides_cattle > 0, I.D / I.hides_cattle, 0.0)
# regions with cattle deforestation but no alpha_econ (no FAOSTAT weights) take the hide-production-weighted mean alpha of the year
for c in ['alpha_econ', 'alpha_mass']:
    wm = I.dropna(subset=[c]).groupby('t').apply(lambda g: np.average(g[c], weights=g.hides))
    I[c + '_filled'] = I[c].isna(); I[c] = I[c].fillna(I.t.map(wm))
I.to_csv(f'{DER}/intensity.csv', index=False)
# deforestation not matched to a hide-producing region (DeDuCE cattle deforestation in regions without FAOSTAT hide output)
nohide = D21.merge(H[['region', 't', 'hides']], on=['region', 't'], how='left')
nohide = nohide[(nohide.hides.isna() | (nohide.hides == 0)) & nohide.t.isin(YEARS)]
info = dict(baci=qinfo, intra_eu_rows_dropped=int(len(intra)), faostat_flags=flags, faostat_unmatched_t=unmatched.round(0).head(10).to_dict(),
            deduce21_unmapped_iso=miss21[miss21 > 0].round(0).to_dict(), deduce20_unmapped_iso=miss20[miss20 > 0].round(0).to_dict(),
            deforestation_without_hide_output_ha=nohide.groupby('t').D.sum().round(0).to_dict(),
            deforestation_without_hide_output_regions=nohide.groupby('region').D.sum().sort_values(ascending=False).head(5).round(0).to_dict(),
            global_hides_t={int(k): float(v) for k, v in H.groupby('t').hides.sum().items()},
            deduce21_cattle_total_ha={int(k): float(v) for k, v in D21.groupby('t').D.sum().items()},
            p_hide={int(k): round(v, 3) for k, v in p_hide.items()}, p_beef_world={int(k): round(v, 3) for k, v in p_beef_world.items()})
json.dump(info, open(f'{RES}/build_info.json', 'w'), indent=1, default=str)
json.dump({'name': name, 'iso3': iso3}, open(f'{DER}/regions.json', 'w'))
print(json.dumps({k: info[k] for k in ['baci', 'faostat_flags', 'faostat_unmatched_t', 'deduce21_unmapped_iso', 'deforestation_without_hide_output_regions']}, indent=1, default=str))
print(I[I.region.isin(['76', '600', '156', '699', EU])].query('t in [2005, 2015, 2023]')[['region', 't', 'hides', 'D', 'ha_per_t', 'alpha_econ', 'alpha_mass']].round(4))
