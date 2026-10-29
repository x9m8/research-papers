"""Build the county panel: Medicare Part D GLP-1 exposure (2019-2024) and QCEW outcomes (2015-2025).
Inputs in data/raw/ (see README and fetch_data.py); outputs data/derived/county_panel.csv,
data/derived/exposure_county_year.csv and results/build.json."""
import json, os
import numpy as np
import pandas as pd
from common import RAW, DER, RES, YEARS_Q, YEARS_D, BASE, END_D, DROP_STATES

info = {}
# ---------- ZIP -> county ----------
xw = pd.read_csv(os.path.join(RAW, 'zcta_county_2020_maxland.csv'), dtype=str)
zip2cty = dict(zip(xw.zcta.str.zfill(5), xw.county_fips.str.zfill(5)))
info['n_zcta'] = len(zip2cty)

# ---------- Part D enrollees by county ----------
en = pd.read_csv(os.path.join(RAW, 'medicare_enrollment_county.csv'), dtype=str)
en['fips'] = en.BENE_FIPS_CD.str.zfill(5)
en['year'] = en.YEAR.astype(int)
for c in ('TOT_BENES', 'PRSCRPTN_DRUG_TOT_BENES', 'AGED_TOT_BENES'):
    en[c] = pd.to_numeric(en[c].str.replace(',', ''), errors='coerce')
en = en[en.year.isin(YEARS_D)][['fips', 'year', 'TOT_BENES', 'PRSCRPTN_DRUG_TOT_BENES', 'AGED_TOT_BENES']]
en.columns = ['fips', 'year', 'mcare', 'partd', 'aged']

# ---------- GLP-1 fills by prescriber county ----------
SEMTIR = {'Semaglutide', 'Tirzepatide'}
rows, cov = [], {}
for y in YEARS_D:
    g = pd.read_csv(os.path.join(RAW, f'partd_glp1_npi_{y}.csv'), dtype=str)
    for c in ('Tot_Clms', 'Tot_30day_Fills'):
        g[c] = pd.to_numeric(g[c], errors='coerce').fillna(0)
    g['fips'] = g.Prscrbr_Zip5.fillna('').str.zfill(5).map(zip2cty)
    geo = pd.read_csv(os.path.join(RAW, f'partd_geo_glp1_{y}.csv'), dtype=str)
    nat = pd.to_numeric(geo.loc[geo.Prscrbr_Geo_Lvl == 'National', 'Tot_30day_Fills'], errors='coerce').sum()
    cov[y] = {'npi_rows': int(len(g)), 'fills_npi_file': float(g.Tot_30day_Fills.sum()), 'fills_national': float(nat),
              'share_of_national_in_npi_file': float(g.Tot_30day_Fills.sum() / nat),
              'share_fills_matched_to_county': float(g.loc[g.fips.notna(), 'Tot_30day_Fills'].sum() / g.Tot_30day_Fills.sum()),
              'fills_by_generic_national': {k: float(v) for k, v in geo[geo.Prscrbr_Geo_Lvl == 'National'].assign(
                  f=lambda d: pd.to_numeric(d.Tot_30day_Fills, errors='coerce')).groupby('Gnrc_Name').f.sum().items()}}
    g['semtir'] = np.where(g.Gnrc_Name.isin(SEMTIR), g.Tot_30day_Fills, 0.0)
    a = g.dropna(subset=['fips']).groupby('fips').agg(glp_fills=('Tot_30day_Fills', 'sum'), glp_clms=('Tot_Clms', 'sum'),
                                                      semtir_fills=('semtir', 'sum')).reset_index()
    # all Part D claims by prescriber county (alternative denominator)
    pz = pd.read_csv(os.path.join(RAW, f'partd_provider_zip_{y}.csv'), dtype={'zip5': str})
    pz['fips'] = pz.zip5.fillna('').str.zfill(5).map(zip2cty)
    pz = pz.dropna(subset=['fips']).groupby('fips').tot_clms.sum().rename('all_clms').reset_index()
    a = pz.merge(a, on='fips', how='left').fillna({'glp_fills': 0, 'glp_clms': 0, 'semtir_fills': 0})
    a['year'] = y
    rows.append(a)
    # state validation: county sums vs the CMS state file
    st = geo[geo.Prscrbr_Geo_Lvl == 'State'].assign(f=lambda d: pd.to_numeric(d.Tot_30day_Fills, errors='coerce')).groupby('Prscrbr_Geo_Cd').f.sum()
    mine = a.assign(s=a.fips.str[:2]).groupby('s').glp_fills.sum()
    j = pd.concat([st.rename('cms'), mine.rename('mine')], axis=1).dropna()
    j = j[j.index.astype(str).str.match(r'^\d\d$') & (j.index.astype(str) <= '56')]
    cov[y]['state_corr_county_sum_vs_cms_state'] = float(np.corrcoef(j.cms, j.mine)[0, 1])
    cov[y]['state_ratio_median'] = float((j.mine / j.cms).median())
info['coverage'] = cov
ex = pd.concat(rows).merge(en, on=['fips', 'year'], how='left')
ex['E'] = 100 * ex.glp_fills / 12 / ex.partd            # full-year-equivalent users per 100 Part D enrollees
ex['E_semtir'] = 100 * ex.semtir_fills / 12 / ex.partd
ex['E_share'] = 1000 * ex.glp_clms / ex.all_clms        # GLP-1 claims per 1,000 Part D claims (prescriber-based)
ex.to_csv(os.path.join(DER, 'exposure_county_year.csv'), index=False)

# ---------- QCEW outcomes ----------
def qcew(ind_codes, key):
    d = pd.concat([pd.read_csv(os.path.join(RAW, f'qcew_{c}.csv'), dtype=str) for c in ind_codes])
    d = d[d.year.astype(int).isin(YEARS_Q)]
    d['year'] = d.year.astype(int)
    if key == 'pharm':      # NAICS 2017 446110 up to 2021, NAICS 2022 456110 from 2022
        d = d[((d.industry_code == '446110') & (d.year <= 2021)) | ((d.industry_code == '456110') & (d.year >= 2022))]
    sup = d.disclosure_code.fillna('') == 'N'
    for c, n in (('annual_avg_emplvl', 'emp'), ('annual_avg_estabs', 'est'), ('total_annual_wages', 'wag')):
        d[f'{key}_{n}'] = pd.to_numeric(d[c], errors='coerce').where(~sup)
    d['fips'] = d.area_fips.str.zfill(5)
    return d[['fips', 'year', f'{key}_emp', f'{key}_est', f'{key}_wag']].drop_duplicates(['fips', 'year'])

q = None
for codes, key in ((['722511'], 'fsr'), (['722513'], 'lsr'), (['446110', '456110'], 'pharm'), (['721'], 'acc'),
                   (['445110'], 'groc'), (['10'], 'tot')):
    d = qcew(codes, key)
    q = d if q is None else q.merge(d, on=['fips', 'year'], how='outer')
q = q[(q.fips.str[:2] <= '56') & ~q.fips.str[:2].isin(DROP_STATES) & ~q.fips.str.endswith('999')]
q.to_csv(os.path.join(DER, 'qcew_county_year.csv'), index=False)

# ---------- wide county file ----------
w = q.pivot(index='fips', columns='year')
w.columns = [f'{a}_{b}' for a, b in w.columns]
e = ex.pivot(index='fips', columns='year', values=['E', 'E_semtir', 'E_share', 'partd', 'aged', 'mcare', 'glp_fills'])
e.columns = [f'{a}_{b}' for a, b in e.columns]
p = w.join(e, how='inner').reset_index()
p = p[~p.fips.str[:2].isin(DROP_STATES)]
p['state'] = p.fips.str[:2]
p['dE'] = p[f'E_{END_D}'] - p[f'E_{BASE}']
p['dE_semtir'] = p[f'E_semtir_{END_D}'] - p[f'E_semtir_{BASE}']
p['dE_share'] = p[f'E_share_{END_D}'] - p[f'E_share_{BASE}']
p.to_csv(os.path.join(DER, 'county_panel.csv'), index=False)
info['n_counties_joined'] = int(len(p))
json.dump(info, open(os.path.join(RES, 'build.json'), 'w'), indent=1)
print(json.dumps(info, indent=1)[:3000])
