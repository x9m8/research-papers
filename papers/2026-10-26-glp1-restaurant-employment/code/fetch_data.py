"""Download and reduce the public inputs into data/raw/ (ordinary machine with internet access).
Mirrors fetch_browser.js, which was used to build the published results because the analysis environment
had no direct internet access. Requires: requests, pandas. Run once: python3 fetch_data.py"""
import io, os, gzip, time
import requests
import pandas as pd
from common import RAW

B = 'https://data.cms.gov/data-api/v1/dataset/'
PD = {2019: '2a6705e6-7a1e-460c-ba22-35249a531918', 2020: '7795fe20-e80e-435a-a9ed-d2d65e05feeb', 2021: 'f68114ed-f854-4ffc-9c6e-ed78b5e2f8d0',
      2022: 'b101b457-ffa4-49bb-8fd9-27c1266086e2', 2023: 'e54db557-cd82-4e91-a0fe-61aad5865d69', 2024: '9552739e-3d05-4c1b-8eff-ecabf391e2e5'}
PROV = {2019: '1f0bef67-2dae-460d-ac47-02866bb3a4bb', 2020: '265b3d0b-495d-424c-a204-5e3b86e4e6d0', 2021: '838f7a4c-0423-4370-8227-588ce9b94b93',
        2022: 'adcdaca6-0c9c-485f-af21-1abc16104d6c', 2023: '42888afe-3b85-4a61-a4ee-091f00bd62bc', 2024: '14d8e8a9-7e9b-4370-a044-bf97c46b4b44'}
GEO = {2019: '73a6335e-f16f-4c81-a84b-6b5a986e2bf8', 2020: '83891e77-99cf-4865-b60a-97703b916e09', 2021: '7dda2a9d-034a-446a-b4b3-e1254e0127b2',
       2022: '1fc57194-a51d-4864-aee6-de0889488151', 2023: '3463648b-1971-478d-84ca-80cadc758153', 2024: 'c8ea3f8e-3a09-4fea-86f2-8902fb4b0920'}
ENR = 'd7fabe1e-d19b-4333-9eff-e80e0643f2fd'
GEN = ['Semaglutide', 'Tirzepatide', 'Liraglutide', 'Dulaglutide', 'Exenatide', 'Exenatide Microspheres', 'Lixisenatide', 'Albiglutide',
       'Insulin Glargine/Lixisenatide', 'Insulin Degludec/Liraglutide']
QIND = {'722511': range(2015, 2026), '722513': range(2015, 2026), '446110': range(2015, 2022), '456110': range(2022, 2026),
        '721': range(2015, 2026), '445110': range(2015, 2026), '10': range(2015, 2026)}
S = requests.Session()


def get_all(ds, params, cols):
    n = S.get(f'{B}{ds}/data/stats', params=params).json()['found_rows']
    out = []
    for off in range(0, n, 5000):
        for t in range(6):
            r = S.get(f'{B}{ds}/data', params={**params, 'column': cols, 'size': 5000, 'offset': off})
            if r.ok:
                out += r.json(); break
            time.sleep(2 * (t + 1))
    assert len(out) == n, (ds, len(out), n)
    return pd.DataFrame(out)


def main():
    os.makedirs(RAW, exist_ok=True)
    for y in PD:
        prov = get_all(PROV[y], {}, 'Prscrbr_NPI,Prscrbr_Zip5,Tot_Clms')
        prov['Tot_Clms'] = pd.to_numeric(prov.Tot_Clms, errors='coerce').fillna(0)
        z = prov.groupby('Prscrbr_Zip5').agg(n_prescribers=('Prscrbr_NPI', 'size'), tot_clms=('Tot_Clms', 'sum')).reset_index()
        z.rename(columns={'Prscrbr_Zip5': 'zip5'}).to_csv(f'{RAW}/partd_provider_zip_{y}.csv', index=False)
        cols = 'Prscrbr_NPI,Prscrbr_State_FIPS,Brnd_Name,Gnrc_Name,Tot_Clms,Tot_30day_Fills,Tot_Benes'
        g = pd.concat([get_all(PD[y], {'filter[Gnrc_Name]': gn}, cols) for gn in GEN])
        g['Prscrbr_Zip5'] = g.Prscrbr_NPI.map(dict(zip(prov.Prscrbr_NPI, prov.Prscrbr_Zip5)))
        g.to_csv(f'{RAW}/partd_glp1_npi_{y}.csv', index=False)
        gc = 'Prscrbr_Geo_Lvl,Prscrbr_Geo_Cd,Prscrbr_Geo_Desc,Brnd_Name,Gnrc_Name,Tot_Prscrbrs,Tot_Clms,Tot_30day_Fills,Tot_Benes'
        pd.concat([get_all(GEO[y], {'filter[Gnrc_Name]': gn}, gc) for gn in GEN]).to_csv(f'{RAW}/partd_geo_glp1_{y}.csv', index=False)
    get_all(ENR, {'filter[BENE_GEO_LVL]': 'County', 'filter[MONTH]': 'Year'},
            'YEAR,BENE_FIPS_CD,BENE_STATE_ABRVTN,TOT_BENES,PRSCRPTN_DRUG_TOT_BENES,AGED_TOT_BENES').to_csv(f'{RAW}/medicare_enrollment_county.csv', index=False)
    keep = ['area_fips', 'own_code', 'industry_code', 'year', 'disclosure_code', 'annual_avg_estabs', 'annual_avg_emplvl', 'total_annual_wages']
    for ind, yrs in QIND.items():
        parts = []
        for y in yrs:
            d = pd.read_csv(io.StringIO(S.get(f'https://data.bls.gov/cew/data/api/{y}/a/industry/{ind}.csv').text), dtype=str)
            d = d[d.area_fips.str.match(r'^\d{5}$') & ~d.area_fips.str.endswith('000') & (d.own_code == '5')]
            parts.append(d[keep])
        pd.concat(parts).to_csv(f'{RAW}/qcew_{ind}.csv', index=False)
    x = pd.read_csv('https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt', sep='|', dtype=str)
    x = x.dropna(subset=['GEOID_ZCTA5_20']).assign(a=lambda d: pd.to_numeric(d.AREALAND_PART))
    x = x.sort_values('a', ascending=False).drop_duplicates('GEOID_ZCTA5_20')
    x[['GEOID_ZCTA5_20', 'GEOID_COUNTY_20']].set_axis(['zcta', 'county_fips'], axis=1).to_csv(f'{RAW}/zcta_county_2020_maxland.csv', index=False)
    open(f'{RAW}/affinity_state_monthly.csv', 'wb').write(S.get(
        'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20State%20-%20Monthly.csv').content)


if __name__ == '__main__':
    main()
