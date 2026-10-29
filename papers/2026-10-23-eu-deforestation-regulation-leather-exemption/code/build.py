"""Assemble the analysis panel: DeDuCE cattle deforestation, FAOSTAT hides and beef, Eurostat Comext EU27 imports."""
import numpy as np, pandas as pd, pycountry
from common import RAW, RES, RHE
# DeDuCE
d = pd.read_csv(f'{RAW}/x9p8-deduce-attrib-cattle.csv')
D = d.pivot_table(index=['ISO', 'Producer country', 'Year'], columns='Commodity',
                  values=['Deforestation risk, amortized (ha)', 'Deforestation attribution, unamortized (ha)'], aggfunc='sum')
D.columns = [('amort_' if 'amortized (ha)' in a and 'risk' in a else 'unamort_') + b.replace(' ', '_').lower() for a, b in D.columns]
D = D.reset_index().rename(columns={'ISO': 'iso3', 'Producer country': 'country', 'Year': 'year'})
D['amort_cattle'] = D.amort_cattle_meat + D.amort_leather; D['unamort_cattle'] = D.unamort_cattle_meat + D.unamort_leather
D['deduce_leather_share'] = D.amort_leather / D.amort_cattle
# FAOSTAT
q = pd.read_csv(f'{RAW}/faostat_qcl_cattle.csv', dtype={'Area Code (M49)': str})
q['m49'] = q['Area Code (M49)'].str.strip("'")
def iso3(m):
    try: return pycountry.countries.get(numeric=m).alpha_3
    except Exception: return None
q['iso3'] = q.m49.map(iso3)
key = {('Raw hides and skins of cattle', 'Production'): 'hides_t', ('Raw hides and skins of cattle', 'Yield/Carcass Weight'): 'hide_kg_head',
       ('Meat of cattle with the bone, fresh or chilled', 'Production'): 'beef_t', ('Meat of cattle with the bone, fresh or chilled', 'Yield/Carcass Weight'): 'carcass_kg_head',
       ('Meat of cattle with the bone, fresh or chilled', 'Producing Animals/Slaughtered'): 'slaughter_head'}
q['var'] = [key.get((i, e)) for i, e in zip(q.Item, q.Element)]
F = q[q['var'].notna() & q.iso3.notna()].pivot_table(index=['iso3', 'Year'], columns='var', values='Value', aggfunc='first').reset_index().rename(columns={'Year': 'year'})
# Comext all partners, HS4
c = pd.read_csv(f'{RAW}/x9p8-comext-eu27-4101-4104-4107.csv', dtype={'product': str, 'partner': str}, keep_default_na=False)  # keep Namibia ('NA')
c['value'] = pd.to_numeric(c.value, errors='coerce')
ext_total = c[c.partner == 'EXT_EU27_2020'].pivot_table(index=['year', 'product'], columns='indicator', values='value', aggfunc='sum').reset_index()
ext_total['t_rhe'] = ext_total.QUANTITY_IN_100KG.fillna(0) / 10 * ext_total['product'].map(RHE)
ext_total.groupby('year').t_rhe.sum().rename('t_rhe_extra_eu_total').to_csv(f'{RES}/extra_eu_total_rhe.csv')
def iso3_2(a):
    try: return pycountry.countries.get(alpha_2=a).alpha_3
    except Exception: return None
c['iso3'] = c.partner.map(iso3_2)
eu = {x.alpha_3 for x in map(lambda a: pycountry.countries.get(alpha_2=a), 'AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE'.split())}
c = c[c.iso3.notna() & ~c.iso3.isin(eu)]
C = c.pivot_table(index=['iso3', 'partner', 'year', 'product'], columns='indicator', values='value', aggfunc='sum').reset_index()
C['t'] = C.QUANTITY_IN_100KG.fillna(0) / 10; C['eur'] = C.VALUE_IN_EUROS.fillna(0)
C['t_rhe'] = C.t * C['product'].map(RHE)
M = C.pivot_table(index=['iso3', 'partner', 'year'], columns='product', values=['t', 't_rhe', 'eur'], aggfunc='sum')
M.columns = [f'{a}_{b}' for a, b in M.columns]; M = M.reset_index().fillna(0)
M['t_rhe'] = M[[f't_rhe_{p}' for p in RHE]].sum(axis=1); M['eur'] = M[[f'eur_{p}' for p in RHE]].sum(axis=1)
# Prices: EU import unit values (EUR/kg), raw hides 4101 from all extra-EU, beef 0201+0202 by origin
h = pd.read_csv(f'{RAW}/x9p8-comext-eu27-hs6-beef-origins-1.csv', dtype={'product': str, 'partner': str}, keep_default_na=False)
h['value'] = pd.to_numeric(h.value, errors='coerce')
h['product'] = h['product'].str.zfill(4); h['hs4'] = h['product'].str[:4]
H = h.pivot_table(index=['partner', 'year', 'hs4'], columns='indicator', values='value', aggfunc='sum').reset_index()
H['kg'] = H.QUANTITY_IN_100KG * 100; H['uv'] = H.VALUE_IN_EUROS / H.kg
hide_uv = H[(H.partner == 'EXT_EU27_2020') & (H.hs4 == '4101')].set_index('year').uv.rename('p_hide_raw')
wb_uv = H[(H.partner == 'EXT_EU27_2020') & (H.hs4 == '4104')].set_index('year').uv.rename('p_wetblue')
beef = H[H.hs4.isin(['0201', '0202'])].groupby(['partner', 'year'])[['VALUE_IN_EUROS', 'kg']].sum().reset_index()
beef['p_beef'] = beef.VALUE_IN_EUROS / beef.kg; beef['iso3'] = beef.partner.map(iso3_2)
MIN_T = 100  # origin beef price used only if the EU imported >= 100 t of beef from that origin that year
beef['p_beef_raw'] = beef.p_beef; beef.loc[beef.kg < MIN_T * 1000, 'p_beef'] = np.nan
# fixed-mix (Laspeyres-type) extra-EU beef price: origin prices weighted by 2005-2007 volume shares, renormalised over origins priced that year
o = beef[(beef.partner != 'EXT_EU27_2020') & beef.p_beef.notna()]
w0 = o[o.year.between(2005, 2007)].groupby('partner').kg.sum(); w0 = w0 / w0.sum()
fm = o.assign(w=o.partner.map(w0)).dropna(subset=['w']).groupby('year').apply(lambda g: np.average(g.p_beef, weights=g.w)).rename('p_beef_fixedmix')
beef_world = beef[beef.partner == 'EXT_EU27_2020'].set_index('year').p_beef.rename('p_beef_world')
P = pd.concat([hide_uv, wb_uv, beef_world, fm], axis=1).reset_index().rename(columns={'index': 'year'})
# Panel
X = M.merge(D, on=['iso3', 'year'], how='left').merge(F, on=['iso3', 'year'], how='left').merge(beef[['iso3', 'year', 'p_beef']], on=['iso3', 'year'], how='left').merge(P, on='year', how='left')
X.to_csv(f'{RES}/panel.csv', index=False); D.to_csv(f'{RES}/deduce_cattle.csv', index=False); P.to_csv(f'{RES}/prices_eu_import.csv', index=False)
print(X[X.year.between(2005, 2022)].groupby('year')[['t_rhe']].sum().T.round(0)); print(P.round(3).to_string())
print('leather share in DeDuCE:', D.deduce_leather_share.min(), D.deduce_leather_share.max())
top = X[X.year.between(2018, 2022)].groupby('iso3').t_rhe.sum().sort_values(ascending=False).head(12); print(top / top.sum())
