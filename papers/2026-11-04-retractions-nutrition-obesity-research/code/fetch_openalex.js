// fetch_openalex.js — step 3b, as run in a Chrome tab (29 October 2026) alongside Pyodide (object py).
// Reads data/derived/citation_dois.json from the Pyodide file system, looks up each DOI in OpenAlex
// (https://api.openalex.org/works, 50 DOIs per request, fields doi, publication_year, cited_by_count, counts_by_year,
// is_retracted) and writes data/derived/openalex.json (record level, not redistributed). fetch_openalex.py does the same in Python.
async function fetchOpenAlex(py, root) {
  const recs = JSON.parse(py.FS.readFile(root + '/data/derived/citation_dois.json', { encoding: 'utf8' }));
  const dois = [...new Set(recs.map(x => x.doi))].filter(d => !/[,|]/.test(d));
  const out = { works: {}, skipped: recs.length - dois.length, failed: [], retrieved: new Date().toISOString() };
  for (let i = 0; i < dois.length; i += 50) {
    const batch = dois.slice(i, i + 50);
    const url = 'https://api.openalex.org/works?per_page=50&select=doi,publication_year,cited_by_count,counts_by_year,is_retracted&filter=doi:' +
      batch.map(encodeURIComponent).join('|');
    let ok = false;
    for (let t = 0; t < 5 && !ok; t++) {
      try {
        const r = await fetch(url);
        if (!r.ok) throw new Error(r.status);
        const j = await r.json();
        for (const w of j.results) {
          const d = (w.doi || '').toLowerCase().replace('https://doi.org/', '');
          const cby = {}; for (const c of w.counts_by_year) cby[c.year] = c.cited_by_count;
          out.works[d] = { cited_by_count: w.cited_by_count, is_retracted: w.is_retracted, publication_year: w.publication_year, counts_by_year: cby };
        }
        ok = true;
      } catch (e) { await new Promise(res => setTimeout(res, 2000 * (t + 1))); }
    }
    if (!ok) out.failed.push(...batch);
    await new Promise(res => setTimeout(res, 150));
  }
  py.FS.writeFile(root + '/data/derived/openalex.json', JSON.stringify(out));
  return Object.keys(out.works).length;
}
