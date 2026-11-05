// fetch_browser.js — QCEW extraction as actually run in a Chrome tab on https://data.bls.gov (28 October 2026).
// The analysis environment had no direct internet access, so the quarterly QCEW industry files were fetched
// same-origin in the browser, reduced to private-ownership county rows for New York (36), New Jersey (34) and
// Pennsylvania (42), and written as one CSV (data/raw/qcew_ny_nj_pa_quarterly.csv) into Pyodide's virtual file
// system, where the Python scripts in code/ were run unchanged. fetch_data.py does the same with `requests`.
// The QCEW open-data API served quarters 2014Q1–2026Q1 at the time of retrieval (earlier years returned 404).
// A 200 response with no matching rows is treated as a failure and retried; persistent failure stops the run.
// (Version 1 of the data was fetched before this check was added; an independent re-fetch reproduced it byte for byte.)
const IND = ['10', '722', '7224', '7225', '722511', '722513'];
const KEEP = ['area_fips', 'own_code', 'industry_code', 'year', 'qtr', 'disclosure_code', 'qtrly_estabs',
  'month1_emplvl', 'month2_emplvl', 'month3_emplvl', 'total_qtrly_wages', 'avg_wkly_wage'];
window.Q = { rows: {}, log: [], done: 0 };
async function one(y, q, i) {
  for (let t = 0; t < 4; t++) {
    try {
      const r = await fetch(`/cew/data/api/${y}/${q}/industry/${i}.csv`);
      if (r.status === 404) { Q.log.push(`404 ${y} ${q} ${i}`); return; }
      if (!r.ok) throw r.status;
      const L = (await r.text()).trim().split('\n');
      const h = L[0].replace(/"/g, '').split(','); const idx = KEEP.map(k => h.indexOf(k)); const out = [];
      for (const l of L.slice(1)) {
        const f = l.replace(/"/g, '').split(','); const a = f[idx[0]];
        if (!/^(36|34|42)\d{3}$/.test(a) || a.endsWith('000') || f[idx[1]] !== '5') continue;   // counties, private ownership
        out.push(idx.map(j => f[j]).join(','));
      }
      if (out.length === 0) throw new Error('HTTP 200 but no matching county rows');   // fail loudly and retry
      Q.rows[`${y}_${q}_${i}`] = out; return;
    } catch (e) { await new Promise(r => setTimeout(r, 2000 * (t + 1))); }
  }
  Q.log.push(`FAIL ${y} ${q} ${i}`);
  throw new Error(`QCEW file ${y} Q${q} ${i} failed or empty after 4 tries`);
}
async function fetchQCEW() {
  const jobs = [];
  for (let y = 2010; y <= 2026; y++) for (let q = 1; q <= 4; q++) for (const i of IND) jobs.push([y, q, i]);
  let k = 0;
  const w = async () => { while (k < jobs.length) { const j = jobs[k++]; await one(...j); Q.done++; } };
  await Promise.all([1, 2, 3, 4, 5, 6].map(w));
  const keys = Object.keys(Q.rows).sort();
  window.CSV = KEEP.join(',') + '\n' + keys.map(k => Q.rows[k].join('\n')).join('\n') + '\n';
  return CSV.length;
}
window.P20 = { fetchQCEW };
