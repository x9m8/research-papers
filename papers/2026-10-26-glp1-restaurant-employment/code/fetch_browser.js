// fetch_browser.js — data extraction run in a Chrome tab on https://data.bls.gov (October 2026).
// The analysis shell had no direct internet access, so the public files were fetched in the browser,
// reduced to the columns and rows the analysis needs, written as CSV into Pyodide's virtual file system
// (data/raw/), and the Python scripts in code/ were run there unchanged. fetch_data.py does the same
// extraction with `requests` for anyone running the package on an ordinary machine.
// Sources: CMS Medicare Part D Prescribers (by Provider and Drug; by Provider), CMS Medicare Monthly
// Enrollment (data.cms.gov data API, CORS-enabled); BLS QCEW open-data API (same origin);
// Census 2020 ZCTA-to-county relationship file (fetched on www2.census.gov, reduced to the county with the
// largest land-area overlap per ZCTA, and carried to this origin through the URL fragment).
const B = 'https://data.cms.gov/data-api/v1/dataset/';
const PD = {2019:'2a6705e6-7a1e-460c-ba22-35249a531918',2020:'7795fe20-e80e-435a-a9ed-d2d65e05feeb',2021:'f68114ed-f854-4ffc-9c6e-ed78b5e2f8d0',2022:'b101b457-ffa4-49bb-8fd9-27c1266086e2',2023:'e54db557-cd82-4e91-a0fe-61aad5865d69',2024:'9552739e-3d05-4c1b-8eff-ecabf391e2e5'};
const PROV = {2019:'1f0bef67-2dae-460d-ac47-02866bb3a4bb',2020:'265b3d0b-495d-424c-a204-5e3b86e4e6d0',2021:'838f7a4c-0423-4370-8227-588ce9b94b93',2022:'adcdaca6-0c9c-485f-af21-1abc16104d6c',2023:'42888afe-3b85-4a61-a4ee-091f00bd62bc',2024:'14d8e8a9-7e9b-4370-a044-bf97c46b4b44'};
const GEO = {2019:'73a6335e-f16f-4c81-a84b-6b5a986e2bf8',2020:'83891e77-99cf-4865-b60a-97703b916e09',2021:'7dda2a9d-034a-446a-b4b3-e1254e0127b2',2022:'1fc57194-a51d-4864-aee6-de0889488151',2023:'3463648b-1971-478d-84ca-80cadc758153',2024:'c8ea3f8e-3a09-4fea-86f2-8902fb4b0920'};
const ENR = 'd7fabe1e-d19b-4333-9eff-e80e0643f2fd';
const GEN = ['Semaglutide','Tirzepatide','Liraglutide','Dulaglutide','Exenatide','Exenatide Microspheres','Lixisenatide','Albiglutide','Insulin Glargine/Lixisenatide','Insulin Degludec/Liraglutide'];
const QYEARS = [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025];
const QIND = ['722511','722513','446110','456110','721','445110','10'];
window.FILES = window.FILES || {};
window.LOG = window.LOG || [];
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function getAll(id, params, cols, conc = 8) {
  const st = await (await fetch(`${B}${id}/data/stats?${params}`)).json();
  const n = st.found_rows, offs = [];
  for (let o = 0; o < n; o += 5000) offs.push(o);
  const res = new Array(offs.length); let k = 0;
  const worker = async () => { while (k < offs.length) { const i = k++;
    for (let t = 0; t < 6; t++) { try { const r = await fetch(`${B}${id}/data?${params}&column=${cols}&size=5000&offset=${offs[i]}`);
      if (!r.ok) throw new Error(r.status); res[i] = await r.json(); break; } catch (e) { await sleep(1500 * (t + 1)); } }
    if (!res[i]) throw new Error('failed ' + id + ' ' + offs[i]); } };
  await Promise.all(Array.from({ length: conc }, worker));
  const flat = res.flat();
  if (flat.length !== n) throw new Error(`row mismatch ${id}: ${flat.length} vs ${n}`);
  return flat;
}
const toCSV = (rows, cols) => cols.join(',') + '\n' + rows.map(r => cols.map(c => { const v = r[c] ?? ''; return /[",]/.test(v) ? '"' + String(v).replace(/"/g, '""') + '"' : v; }).join(',')).join('\n') + '\n';
async function fetchCMS() {
  for (const y of Object.keys(PD)) {
    // Provider file (about 1.4 million prescribers a year): keep only what the analysis needs —
    // ZIP-level totals of all Part D claims, and each prescriber's ZIP for the GLP-1 join below.
    const pc = 'Prscrbr_NPI,Prscrbr_Zip5,Tot_Clms';
    const prov = await getAll(PROV[y], 'x=1', pc);
    const zipOf = new Map(), zt = new Map();
    for (const r of prov) { zipOf.set(r.Prscrbr_NPI, r.Prscrbr_Zip5);
      const z = zt.get(r.Prscrbr_Zip5) || [0, 0]; z[0] += 1; z[1] += +r.Tot_Clms || 0; zt.set(r.Prscrbr_Zip5, z); }
    FILES[`partd_provider_zip_${y}.csv`] = 'zip5,n_prescribers,tot_clms\n' + [...zt].map(([k, v]) => `${k},${v[0]},${v[1]}`).join('\n') + '\n';
    LOG.push(`prov ${y} ${prov.length} zips ${zt.size}`);
    let glp = [];
    const gc = 'Prscrbr_NPI,Prscrbr_State_FIPS,Brnd_Name,Gnrc_Name,Tot_Clms,Tot_30day_Fills,Tot_Benes';
    for (const g of GEN) glp = glp.concat(await getAll(PD[y], 'filter[Gnrc_Name]=' + encodeURIComponent(g), gc));
    for (const r of glp) r.Prscrbr_Zip5 = zipOf.get(r.Prscrbr_NPI) || '';
    FILES[`partd_glp1_npi_${y}.csv`] = toCSV(glp, gc.split(',').concat(['Prscrbr_Zip5'])); LOG.push(`glp ${y} ${glp.length}`);
    const geoc = 'Prscrbr_Geo_Lvl,Prscrbr_Geo_Cd,Prscrbr_Geo_Desc,Brnd_Name,Gnrc_Name,Tot_Prscrbrs,Tot_Clms,Tot_30day_Fills,Tot_Benes';
    let geo = [];
    for (const g of GEN) geo = geo.concat(await getAll(GEO[y], 'filter[Gnrc_Name]=' + encodeURIComponent(g), geoc));
    FILES[`partd_geo_glp1_${y}.csv`] = toCSV(geo, geoc.split(',')); LOG.push(`geo ${y} ${geo.length}`);
  }
  const ec = 'YEAR,BENE_FIPS_CD,BENE_STATE_ABRVTN,TOT_BENES,PRSCRPTN_DRUG_TOT_BENES,AGED_TOT_BENES';
  const enr = await getAll(ENR, 'filter[BENE_GEO_LVL]=County&filter[MONTH]=Year', ec);
  FILES['medicare_enrollment_county.csv'] = toCSV(enr, ec.split(',')); LOG.push(`enr ${enr.length}`);
}
async function fetchQCEW() {
  const keep = ['area_fips','own_code','industry_code','year','disclosure_code','annual_avg_estabs','annual_avg_emplvl','total_annual_wages'];
  for (const ind of QIND) { const parts = [];
    for (const y of QYEARS) {
      const r = await fetch(`/cew/data/api/${y}/a/industry/${ind}.csv`);
      if (!r.ok) { LOG.push(`qcew ${ind} ${y} HTTP ${r.status}`); continue; }
      const lines = (await r.text()).trim().split('\n'); const h = lines[0].replace(/"/g, '').split(',');
      const idx = keep.map(k => h.indexOf(k));
      for (const L of lines.slice(1)) { const f = L.replace(/"/g, '').split(',');
        const a = f[idx[0]], own = f[idx[1]];
        if (!/^\d{5}$/.test(a) || a.endsWith('000') || own !== '5') continue;   // counties, private ownership
        parts.push(idx.map(i => f[i]).join(',')); }
    }
    FILES[`qcew_${ind}.csv`] = keep.join(',') + '\n' + parts.join('\n') + '\n'; LOG.push(`qcew ${ind} ${parts.length}`);
  }
}
async function loadXwalk() {
  const b64 = localStorage.getItem('p11_xwalk_b64').split('#')[0];   // the BLS page appends its own fragment
  const bin = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
  const txt = await new Response(new Blob([bin]).stream().pipeThrough(new DecompressionStream('gzip'))).text();
  FILES['zcta_county_2020_maxland.csv'] = 'zcta,county_fips\n' + txt + '\n'; LOG.push('xwalk ' + txt.split('\n').length);
}
window.P11 = { fetchCMS, fetchQCEW, loadXwalk };
