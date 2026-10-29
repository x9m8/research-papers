"""Assemble the county files.
 derived/county_base.csv : reproduction file. Store counts and recreation facilities for 2007 (Food Environment Atlas,
     Feb 2014 release; the Nov 2012 release carries slightly different 2007 counts), farmers' markets 2009, adult obesity 2009,
     low-income-low-access 2010, natural amenities, milk:soda price ratio 2010, demographics 2010; plus the 2009 store
     counts from the Nov 2012 release (columns *_09) for the 'as described' variant.
 derived/county2016.csv : update file (2016 counts, PLACES obesity for BRFSS 2018).
Also writes results/build_meta.json."""
import json, zipfile, io, os
import numpy as np, pandas as pd
from common import RAW, DER, dump

def atlas_xls(path, sheets):
    x = pd.ExcelFile(path); d = None
    for s in sheets:
        df = x.parse(s); df['fips'] = df.FIPS.astype(int); df = df.drop(columns=['FIPS']).drop_duplicates('fips')  # Broomfield CO (08014) is listed twice
        d = df if d is None else d.merge(df.drop(columns=['State', 'County']), on='fips', how='outer')
    return d

A = atlas_xls(f'{RAW}/atlas_feb2014.xls', ['STORES', 'RESTAURANTS', 'HEALTH', 'ACCESS', 'LOCAL', 'PRICES_TAXES', 'SOCIOECONOMIC'])
B = atlas_xls(f'{RAW}/atlas_nov2012.xls', ['STORES', 'RESTAURANTS', 'HEALTH'])
sup = pd.read_excel(f'{RAW}/atlas_nov2012.xls', 'Supplemental Data - County')
sup['fips'] = sup['FIPS Code'].astype(int); sup = sup.drop_duplicates('fips')
A = A.merge(sup[['fips', '2010 Census Population']].rename(columns={'2010 Census Population': 'pop10'}), on='fips', how='left')
A = A.merge(B[['fips', 'GROC09', 'SUPERC09', 'CONVS09', 'SPECS09', 'FFR09', 'FSR09', 'RECFAC09']], on='fips', how='left')

# ---- ACS 5-year tables from data.census.gov
acs = json.load(open(f'{RAW}/acs/acs5_county_tables.json'))
def acs_tab(key, src=None):
    rows = (src or acs)[key]; df = pd.DataFrame(rows[1:], columns=rows[0])
    df['fips'] = df.GEO_ID.str[-5:].astype(int)
    return df.set_index('fips')
def acs_vars(y, src=None):
    src = src or acs
    g = acs_tab(f'{y}_B19083', src); c = acs_tab(f'{y}_B08301', src); e = acs_tab(f'{y}_B15002', src); p = acs_tab(f'{y}_B01003', src)
    num = lambda df, v: pd.to_numeric(df[v], errors='coerce')
    out = pd.DataFrame(index=p.index)
    out['gini'] = num(g, 'B19083_001E')
    tot = num(c, 'B08301_001E')
    out['pct_drive'] = 100 * num(c, 'B08301_002E') / tot          # car, truck or van (alone or carpool)
    out['pct_drovealone'] = 100 * num(c, 'B08301_003E') / tot
    out['pct_transit'] = 100 * num(c, 'B08301_010E') / tot
    out['pct_walk'] = 100 * num(c, 'B08301_019E') / tot
    out['pct_drive_transit'] = out.pct_drovealone + out.pct_transit   # Table 9 split variable (see manuscript)
    out['pct_anycar_transit'] = out.pct_drive + out.pct_transit
    out['bach_only'] = 100 * (num(e, 'B15002_015E') + num(e, 'B15002_032E')) / num(e, 'B15002_001E')
    out['bach'] = 100 * sum(num(e, f'B15002_{k:03d}E') for k in (15, 16, 17, 18, 32, 33, 34, 35)) / num(e, 'B15002_001E')
    out['pop_acs'] = num(p, 'B01003_001E')
    return out
acs10 = acs_vars('2010')

geo = json.load(open(f'{RAW}/geo/geojson-counties-fips.json'))
area = pd.Series({int(f['id']): f['properties']['CENSUSAREA'] for f in geo['features']}, name='sqmi')
ex = pd.read_csv(f'{DER}/exits_osm.csv').set_index('fips') if os.path.exists(f'{DER}/exits_osm.csv') else pd.DataFrame({'exits_osm': [], 'exits_osm_uniqref': []})

def add_rfei(df, sfx=''):
    g, sc, cv, sp, ff, fm = (df['groc' + sfx], df['superc' + sfx], df['convs' + sfx], df['specs' + sfx], df['ffr' + sfx], df['fmrkt'])
    defs = {'trad': (ff + cv, g), 'e1': (ff + cv + sc, g + fm + sp), 'e2': (ff + cv, g + fm + sp + sc)}
    for k, (n, m) in defs.items():
        df[f'rfei_{k}{sfx}'] = (n / m.where(m > 0))
        df[f'rfei_{k}{sfx}_p1'] = (n + 1) / (m + 1)               # sensitivity: add one to numerator and denominator
        df[f'lrfei_{k}{sfx}'] = np.log(df[f'rfei_{k}{sfx}_p1'])
        df[f'den_{k}{sfx}'] = m; df[f'num_{k}{sfx}'] = n
    df['tot_outlets' + sfx] = g + sc + cv + sp + ff + fm
    df['ffr_pth' + sfx] = 1e4 * ff / df.popx
    df['unh_pth' + sfx] = 1e4 * (ff + cv) / df.popx
    df['hea_pth' + sfx] = 1e4 * g / df.popx
    return df

d = pd.DataFrame({'fips': A.fips, 'state': A.State, 'county': A.County})
d['stfips'] = d.fips // 1000
d['obese'] = A.PCT_OBESE_ADULTS09
for v in ('groc', 'superc', 'convs', 'specs', 'ffr', 'fsr'):
    d[v] = A[v.upper() + '07']; d[v + '_09'] = A[v.upper() + '09']
d['fmrkt'] = A.FMRKT09
d['recfac'] = A.RECFAC07; d['recfac_09'] = A.RECFAC09
d['natamen'] = A.NATAMEN; d['milksoda'] = A.MILK_SODA_PRICE10; d['lila'] = A.PCT_LACCESS_LOWI10
d['pct_black'] = A.PCT_NHBLACK10; d['pct_hisp'] = A.PCT_HISP10; d['povrate'] = A.POVRATE10; d['medhhinc'] = A.MEDHHINC10
d['pop10'] = A.pop10; d['pop65'] = A.PCT_65OLDER10 / 100 * A.pop10; d['metro'] = A.METRO13
d = d.merge(area, left_on='fips', right_index=True, how='left').merge(acs10, left_on='fips', right_index=True, how='left')
d = d.merge(ex, left_on='fips', right_index=True, how='left')
d['popx'] = d.pop10
d = add_rfei(d); d = add_rfei(d, '_09')
d.to_csv(f'{DER}/county_base.csv', index=False)

# ---- Update: 2016 store counts (Atlas July 2025 release), PLACES 2020 release (BRFSS 2018) obesity, ACS 2014-2018.
# In this release, counts that are absent from County Business Patterns are coded -9999 (2016 has no zeros at all),
# and 2020 counts below 3 are suppressed, so 2020 ratios cannot be formed for small counties. We use 2016 and treat
# -9999 in 2016 counts as zero (flag 'any_na16' marks counties where that matters; dropped in a sensitivity check).
z = zipfile.ZipFile(f'{RAW}/atlas_2025_csv.zip')
L = pd.read_csv(z.open('StateAndCountyData.csv'), dtype={'FIPS': str}, encoding='utf-8-sig')
cnt16 = ['GROC16', 'SUPERC16', 'CONVS16', 'SPECS16', 'FFR16', 'FSR16']
need = cnt16 + ['FMRKT18', 'RECFAC16', 'PCT_LACCESS_LOWI15', 'PCT_NHBLACK20', 'PCT_HISP20', 'PCT_65OLDER20', 'POVRATE21']
W = L[L.Variable_Code.isin(need)].pivot_table(index='FIPS', columns='Variable_Code', values='Value', aggfunc='first')
W.index = W.index.astype(int)
na16 = (W[cnt16 + ['FMRKT18', 'RECFAC16']] == -9999)
W[cnt16 + ['FMRKT18', 'RECFAC16']] = W[cnt16 + ['FMRKT18', 'RECFAC16']].where(~na16, 0)
W = W.where(W > -8000)
P = {}
for blk in open(f'{RAW}/places_county_obesity_2018_2019.csv').read().split('#release ')[1:]:
    rid, body = blk.split('\n', 1); t = pd.read_csv(io.StringIO(body)); t.columns = [c.lower() for c in t.columns]
    t['fips'] = t.countyfips.astype(int); P[rid] = t.set_index('fips')
acs18 = acs_vars('2018', src=json.load(open(f'{RAW}/acs/acs5_county_tables_2018.json')))
e = pd.DataFrame({'fips': W.index}); e['stfips'] = e.fips // 1000
e['obese'] = e.fips.map(P['mssc-ksj7'].obesity_adjprev); e['obese_crude'] = e.fips.map(P['mssc-ksj7'].obesity_crudeprev)
for v, s in [('groc', 'GROC16'), ('superc', 'SUPERC16'), ('convs', 'CONVS16'), ('specs', 'SPECS16'), ('ffr', 'FFR16'), ('fsr', 'FSR16'), ('fmrkt', 'FMRKT18')]:
    e[v] = e.fips.map(W[s])
e['any_na16'] = e.fips.map(na16[['GROC16', 'SUPERC16', 'CONVS16', 'SPECS16', 'FFR16']].any(axis=1))
e['recfac'] = e.fips.map(W.RECFAC16); e['lila'] = e.fips.map(W.PCT_LACCESS_LOWI15)
e['pct_black'] = e.fips.map(W.PCT_NHBLACK20); e['pct_hisp'] = e.fips.map(W.PCT_HISP20); e['povrate'] = e.fips.map(W.POVRATE21)
e = e.merge(acs18, left_on='fips', right_index=True, how='left')
e['pop65'] = e.fips.map(W.PCT_65OLDER20) / 100 * e.pop_acs
e = e.merge(d[['fips', 'natamen', 'milksoda', 'sqmi', 'exits_osm', 'exits_osm_uniqref', 'state']], on='fips', how='left')
e['popx'] = e.pop_acs
e = add_rfei(e)
e.to_csv(f'{DER}/county2016.csv', index=False)

c = d[d.natamen.notna()]
dump({'atlas_rows': len(d), 'n_rfei_trad_07_contig': int(c.rfei_trad.notna().sum()), 'n_rfei_e1_07_contig': int(c.rfei_e1.notna().sum()),
      'n_rfei_e2_07_contig': int(c.rfei_e2.notna().sum()), 'n_rfei_trad_09_contig': int(c.rfei_trad_09.notna().sum()),
      'n_rfei_e1_09_contig': int(c.rfei_e1_09.notna().sum()), 'n_rfei_e2_09_contig': int(c.rfei_e2_09.notna().sum()), 'natamen_nonmissing': int(d.natamen.notna().sum()),
      'obese09_nonmissing': int(d.obese.notna().sum()), 'groc07_zero_contig': int((c.groc == 0).sum()), 'den1_07_zero_contig': int((c.den_e1 == 0).sum()),
      'den2_07_zero_contig': int((c.den_e2 == 0).sum()),
      'places_counties_2018': int(e.obese.notna().sum()), 'rows_2016': len(e),
      'counts16_minus9999_any': int(e.any_na16.sum()),
      'groc20_suppressed': int((L[L.Variable_Code == 'GROC20'].Value == -9999).sum()),
      'superc20_suppressed': int((L[L.Variable_Code == 'SUPERC20'].Value == -9999).sum())}, 'build_meta.json')
print(d.describe().T.to_string()); print(e.describe().T.to_string())
