// fetch_browser.js — the data fetch actually run in a Chrome tab on https://data.ny.gov/
// on 2 November 2026. Both sources allow cross-origin fetch() (CORS), so no WordPress
// relay or download-to-disk step was used; the resulting objects were written straight
// into a Pyodide file system in the same tab (see README.md and results/provenance.md)
// and build_panel.py / analysis.py ran there unchanged.
//
// Run this in the DevTools console (or via an automation tool's javascript-exec
// action) on any https://data.ny.gov/ page; data.ny.gov itself is same-origin for the
// first fetch, and both data.ny.gov and www.ncei.noaa.gov serve Access-Control-Allow-Origin: *.

window.FETCH = { beach: null, jfk: null, isp: null, log: [] };

async function fetchAllBeach() {
  // All 3,301 Long Island rows fit in a single Socrata page (API default/max is well
  // above 3,301 at $limit=5000), so no $offset pagination was needed in practice.
  const base = 'https://data.ny.gov/resource/wwwd-za77.json';
  const r = await fetch(`${base}?$where=region='Long Island'&$limit=5000&$order=:id`);
  const j = await r.json();
  FETCH.beach = j;
  FETCH.log.push('beach n=' + j.length);
}

async function fetchStation(id, name) {
  const url = `https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries` +
    `&stations=${id}&startDate=2000-01-01&endDate=2025-12-31&dataTypes=PRCP,SNOW&format=json&units=metric`;
  const r = await fetch(url);
  const j = await r.json();
  FETCH[name] = j;
  FETCH.log.push(name + ' n=' + j.length);
}

async function fetchAll() {
  await Promise.all([
    fetchAllBeach(),
    fetchStation('USW00094789', 'jfk'),   // JFK International Airport, NY (Nassau-side proxy)
    fetchStation('USW00004781', 'isp'),   // Islip-LI MacArthur Airport, NY (Suffolk-side proxy)
  ]);
  return FETCH.log;
}

// Then, in the same tab, after loading Pyodide (cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js):
//
//   window.pyodide = await loadPyodide();
//   await pyodide.loadPackage(['pandas', 'numpy', 'scipy', 'statsmodels']);
//   pyodide.FS.mkdirTree('/data/raw');
//   pyodide.FS.writeFile('/data/raw/beach_water_testing_li.json', JSON.stringify(FETCH.beach));
//   pyodide.FS.writeFile('/data/raw/ncei_jfk_USW00094789.json', JSON.stringify(FETCH.jfk));
//   pyodide.FS.writeFile('/data/raw/ncei_isp_USW00004781.json', JSON.stringify(FETCH.isp));
//
// and code/common.py, code/build_panel.py, code/analysis.py were written to /code/*.py
// in the same Pyodide file system and imported and run there (sys.path.insert(0, '/code')).
