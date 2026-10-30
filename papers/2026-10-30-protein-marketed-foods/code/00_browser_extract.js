// 00_browser_extract.js -- record of the extraction actually run (Chrome, 22 October 2026) on the official
// USDA FoodData Central Branded Foods CSV release of 2026-04-30:
//   https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_csv_2026-04-30.zip  (448,767,220 bytes)
// The build environment's shell could not reach fdc.nal.usda.gov, so the zip was read in a browser tab on that site,
// decompressed with the native DecompressionStream('deflate-raw'), parsed as CSV, reduced, gzipped and moved to the
// shell in chunks. Run in a page on https://fdc.nal.usda.gov/ (same origin as the zip). Outputs are the four files in
// data/raw/ (fdc_branded_extract_main.tsv.gz, fdc_branded_extract_ingredients.tsv.gz, fdc_branded_summary_counts.tsv.gz,
// sr_legacy_extract.tsv.gz). Anyone with the zip can reproduce them with this script or any CSV tool following the same rules.

const ZU = 'https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_csv_2026-04-30.zip';
let ZB, ZF;
async function loadZip(url) {             // whole zip in memory, then read the central directory (zip64-aware)
  ZB = new Uint8Array(await (await fetch(url)).arrayBuffer());
  const dv = new DataView(ZB.buffer); let e = -1;
  for (let i = ZB.length - 22; i >= 0; i--) if (dv.getUint32(i, true) === 0x06054b50) { e = i; break; }
  let cdOff = dv.getUint32(e + 16, true);
  for (let i = e - 20; i >= 0 && i > e - 100; i--) if (dv.getUint32(i, true) === 0x07064b50) { cdOff = Number(new DataView(ZB.buffer, Number(dv.getBigUint64(i + 8, true))).getBigUint64(48, true)); break; }
  ZF = []; let p = cdOff;
  while (dv.getUint32(p, true) === 0x02014b50) {
    let cs = dv.getUint32(p + 20, true), us = dv.getUint32(p + 24, true), lo = dv.getUint32(p + 42, true);
    const nl = dv.getUint16(p + 28, true), el = dv.getUint16(p + 30, true), kl = dv.getUint16(p + 32, true);
    const name = new TextDecoder().decode(ZB.subarray(p + 46, p + 46 + nl));
    let q = p + 46 + nl; const qe = q + el;
    while (q < qe) { const id = dv.getUint16(q, true), sz = dv.getUint16(q + 2, true); if (id === 1) { let r = q + 4;
      if (us === 0xffffffff) { us = Number(dv.getBigUint64(r, true)); r += 8; } if (cs === 0xffffffff) { cs = Number(dv.getBigUint64(r, true)); r += 8; }
      if (lo === 0xffffffff) { lo = Number(dv.getBigUint64(r, true)); r += 8; } } q += 4 + sz; }
    ZF.push({ name, cs, us, lo }); p = qe + kl;
  }
}

async function streamCSV(fname, onRow) {  // RFC-4180 CSV (quoted fields, "" escapes, embedded newlines)
  const f = ZF.find(x => x.name.endsWith('/' + fname)); const hv = new DataView(ZB.buffer, f.lo, 30);
  const start = f.lo + 30 + hv.getUint16(26, true) + hv.getUint16(28, true);
  const rd = new Blob([ZB.subarray(start, start + f.cs)]).stream().pipeThrough(new DecompressionStream('deflate-raw')).pipeThrough(new TextDecoderStream()).getReader();
  let header = null, fields = [], field = '', inQ = false, pendQ = false, n = 0;
  for (;;) { const { value: s, done } = await rd.read(); if (done) break; let i = 0, seg = 0;
    if (pendQ) { pendQ = false; if (s.charCodeAt(0) === 34) { field += '"'; inQ = true; i = 1; seg = 1; } }
    for (; i < s.length; i++) { const c = s.charCodeAt(i);
      if (inQ) { if (c === 34) { if (i + 1 < s.length) { if (s.charCodeAt(i + 1) === 34) { field += s.slice(seg, i + 1); i++; seg = i + 1; } else { field += s.slice(seg, i); inQ = false; seg = i + 1; } } else { field += s.slice(seg, i); inQ = false; seg = i + 1; pendQ = true; } } }
      else if (c === 34) { inQ = true; seg = i + 1; }
      else if (c === 44) { field += s.slice(seg, i); fields.push(field); field = ''; seg = i + 1; }
      else if (c === 10) { field += s.slice(seg, i); fields.push(field); field = ''; seg = i + 1; if (fields.length > 1 || fields[0] !== '') { if (!header) header = fields; else { onRow(fields, header); n++; } } fields = []; }
      else if (c === 13) { field += s.slice(seg, i); seg = i + 1; } }
    if (seg < s.length) field += s.slice(seg); }
  return { n, header };
}

const KEEP = ['fdc_id','brand_owner','brand_name','subbrand_name','gtin_upc','ingredients','not_a_significant_source_of','serving_size','serving_size_unit',
  'household_serving_fulltext','branded_food_category','data_source','package_weight','modified_date','available_date','market_country','discontinued_date',
  'preparation_state_code','trade_channel','short_description'];
const NUTS = { '1003': 'protein', '1004': 'fat', '1005': 'carb', '1008': 'kcal', '1093': 'sodium', '1235': 'added_sugar', '2000': 'sugars', '1258': 'satfat', '1079': 'fiber', '1253': 'chol', '1257': 'transfat' };

async function run() {
  await loadZip(ZU);
  // 1. branded_food.csv: keep the latest record (max fdc_id) per gtin_upc  -> 1,999,950 rows, 465,110 GTINs
  const BF = new Map(); let idx;
  await streamCSV('branded_food.csv', (f, h) => { idx = idx || KEEP.map(k => h.indexOf(k)); const g = f[idx[4]], cur = BF.get(g); if (!cur || +cur[0] < +f[idx[0]]) BF.set(g, idx.map(j => f[j])); });
  const IDS = new Set([...BF.values()].map(r => r[0]));
  // 2. food.csv: description, publication_date
  const DESC = new Map(); let ix;
  await streamCSV('food.csv', (f, h) => { ix = ix || ['fdc_id', 'description', 'publication_date', 'data_type'].map(k => h.indexOf(k)); if (IDS.has(f[ix[0]])) DESC.set(f[ix[0]], [f[ix[1]], f[ix[2]], f[ix[3]]]); });
  // 3. food_nutrient.csv: selected nutrients (amount per 100 g or 100 ml) for the kept records
  const FN = new Map(); let jx;
  await streamCSV('food_nutrient.csv', (f, h) => { jx = jx || ['fdc_id', 'nutrient_id', 'amount'].map(k => h.indexOf(k)); const k = NUTS[f[jx[1]]]; if (!k || !IDS.has(f[jx[0]])) return; const o = FN.get(f[jx[0]]) || {}; o[k] = f[jx[2]]; FN.set(f[jx[0]], o); });
  // 4. categories in scope: >= 20 products with "protein" in description/brand/sub-brand among US, not-discontinued records
  const K = Object.fromEntries(KEEP.map((k, i) => [k, i])); const cnt = {};
  for (const r of BF.values()) { if (!['United States', 'US'].includes(r[K.market_country]) || r[K.discontinued_date]) continue;
    const d = (DESC.get(r[0]) || [''])[0]; if (/protein/i.test(d + ' ' + r[K.brand_name] + ' ' + r[K.subbrand_name])) cnt[r[K.branded_food_category]] = (cnt[r[K.branded_food_category]] || 0) + 1; }
  const CATS = new Set(Object.keys(cnt).filter(c => cnt[c] >= 20));
  // 5. outputs: (a) every record in a scope category or with "protein" in its name (any country/status): metadata + nutrients;
  //    (b) the ingredient statements of the same records; (c) counts of all latest-GTIN records by category x country x status x year x flags
  const clean = s => (s || '').replace(/[\t\r\n]+/g, ' ').trim();
  const bcols = ['fdc_id','gtin_upc','brand_owner','brand_name','subbrand_name','branded_food_category','serving_size','serving_size_unit','household_serving_fulltext',
    'package_weight','available_date','modified_date','market_country','discontinued_date','not_a_significant_source_of','data_source','trade_channel'];
  const NK = ['protein','fat','carb','kcal','sodium','added_sugar','sugars','satfat','fiber','chol','transfat'];
  const L = [['in_scope', ...bcols, 'description', 'publication_date', ...NK].join('\t')], I = ['fdc_id\tingredients'], summ = {};
  for (const r of BF.values()) { const id = r[0], d = DESC.get(id) || ['', '', ''], n = FN.get(id) || {};
    const inscope = CATS.has(r[K.branded_food_category]), hasP = /protein/i.test(d[0] + ' ' + r[K.brand_name] + ' ' + r[K.subbrand_name]);
    const key = [r[K.branded_food_category], r[K.market_country], r[K.discontinued_date] ? 1 : 0, (r[K.available_date] || '').slice(0, 4), hasP ? 1 : 0, n.protein !== undefined ? 1 : 0, n.added_sugar !== undefined ? 1 : 0].join('\t');
    summ[key] = (summ[key] || 0) + 1;
    if (!(inscope || hasP)) continue;
    L.push([inscope ? 1 : 0, ...bcols.map(k => clean(r[K[k]])), clean(d[0]), d[1], ...NK.map(k => n[k] ?? '')].join('\t'));
    I.push(id + '\t' + clean(r[K.ingredients])); }
  const S = ['category\tmarket_country\tdiscontinued\tavail_year\tprotein_text\thas_protein\thas_added_sugar\tn', ...Object.entries(summ).map(([k, v]) => k + '\t' + v)];
  const gz = async t => new Uint8Array(await new Response(new Blob([t]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer());
  return { main: await gz(L.join('\n')), ing: await gz(I.join('\n')), summary: await gz(S.join('\n')) };
}
// SR Legacy (FoodData_Central_sr_legacy_food_csv_2018-04.zip): food.csv (fdc_id, description, food_category_id) and food_nutrient.csv rows for
// nutrient ids 1003, 1004, 1005, 1008, 1093, 1258, 1079, 2000, 1235, written as one TSV with a '#NUTRIENTS' separator -> sr_legacy_extract.tsv.gz.
// Portion weights used in common.py were read from that zip's food_portion.csv (large egg 50 g; milk 1 quart 976 g; yogurt 8-oz container 227 g).
