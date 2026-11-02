// 00_nhanes_aggregate.js
// Run in a browser tab open on https://wwwn.cdc.gov/ (same-origin fetch of the NHANES public XPT files).
// Reads DEMO and BMX files for each continuous NHANES cycle, parses SAS XPORT v5, and returns
// weighted aggregates (no individual records leave the browser). Output: CSV text, one row per
// cycle x sex x age set x pregnancy rule, plus one row per cycle with population-mean IOM energy
// requirements. Usage in the console:  const csv = await runAll(); console.log(csv)
// Written for: Kalafatis (2026), food waste revisited. Deterministic; no random draws.

function parseXPT(buf) {
  const u = new Uint8Array(buf), td = new TextDecoder('latin1');
  const s = (o, l) => td.decode(u.subarray(o, o + l));
  let p = -1;
  for (let i = 0; i < u.length - 80; i += 80) { if (s(i, 48) === 'HEADER RECORD*******NAMESTR HEADER RECORD!!!!!!!') { p = i; break; } }
  if (p < 0) throw new Error('no NAMESTR header');
  const nvar = parseInt(s(p + 54, 4), 10);
  const vars = []; let q = p + 80;
  for (let k = 0; k < nvar; k++) {
    const o = q + k * 140;
    const ntype = (u[o] << 8) | u[o + 1];
    const nlng = (u[o + 4] << 8) | u[o + 5];
    const name = s(o + 8, 8).trim();
    const npos = (u[o + 84] << 24) | (u[o + 85] << 16) | (u[o + 86] << 8) | u[o + 87];
    vars.push({ name, ntype, nlng, npos });
  }
  q = q + nvar * 140; q = Math.ceil(q / 80) * 80;            // pad to 80
  if (s(q, 48) !== 'HEADER RECORD*******OBS     HEADER RECORD!!!!!!!') throw new Error('no OBS header');
  const d0 = q + 80;
  const obslen = vars.reduce((a, v) => Math.max(a, v.npos + v.nlng), 0);
  const nobs = Math.floor((u.length - d0) / obslen);
  const ibm = (o, n) => {
    const b0 = u[o];
    let rest0 = true; for (let i = 1; i < n; i++) if (u[o + i] !== 0) { rest0 = false; break; }
    if (rest0 && (b0 === 0x2E || b0 === 0x5F || (b0 >= 0x41 && b0 <= 0x5A))) return NaN;   // missing
    if (rest0 && b0 === 0) return 0;
    const sign = b0 & 0x80 ? -1 : 1, ex = (b0 & 0x7f) - 64;
    let m = 0; for (let i = 1; i < n; i++) m = m * 256 + u[o + i];
    m = m / Math.pow(2, 8 * (n - 1));
    return sign * m * Math.pow(16, ex);
  };
  const cols = {};
  for (const v of vars) {
    if (v.ntype !== 1) continue;
    const a = new Float64Array(nobs);
    for (let r = 0; r < nobs; r++) a[r] = ibm(d0 + r * obslen + v.npos, v.nlng);
    cols[v.name] = a;
  }
  // drop trailing blank-padding pseudo-rows (SEQN missing or 0)
  let n = nobs; while (n > 0 && !(cols.SEQN[n - 1] > 0)) n--;
  for (const k in cols) cols[k] = cols[k].subarray(0, n);
  return { n, cols };
}

const CYCLES = [
  ['1999-2000', '1999', '', 'WTMEC2YR'], ['2001-2002', '2001', '_B', 'WTMEC2YR'], ['2003-2004', '2003', '_C', 'WTMEC2YR'],
  ['2005-2006', '2005', '_D', 'WTMEC2YR'], ['2007-2008', '2007', '_E', 'WTMEC2YR'], ['2009-2010', '2009', '_F', 'WTMEC2YR'],
  ['2011-2012', '2011', '_G', 'WTMEC2YR'], ['2013-2014', '2013', '_H', 'WTMEC2YR'], ['2015-2016', '2015', '_I', 'WTMEC2YR'],
  ['2017-2018', '2017', '_J', 'WTMEC2YR'], ['2017-2020pre', '2017', 'P_', 'WTMECPRP'], ['2021-2023', '2021', '_L', 'WTMEC2YR'],
];
const url = (yr, suf, f) => suf === 'P_' ? `/Nchs/Data/Nhanes/Public/${yr}/DataFiles/P_${f}.xpt` : `/Nchs/Data/Nhanes/Public/${yr}/DataFiles/${f}${suf}.xpt`;

// IOM (2005) estimated energy requirement, sedentary (PA = 1.0) and low-active PA coefficients.
function eer(sex, age, months, wt, htm, pal) {
  if (!(wt > 0)) return NaN;
  if (age < 3) {
    const mo = age < 1 ? (months >= 0 ? months : 6) : 24;
    const dep = age >= 1 ? 20 : (mo <= 3 ? 175 : (mo <= 6 ? 56 : 22));
    return 89 * wt - 100 + dep;
  }
  if (!(htm > 0)) return NaN;
  if (age <= 18) {
    const add = age <= 8 ? 20 : 25;
    if (sex === 1) { const PA = pal ? 1.13 : 1.0; return 88.5 - 61.9 * age + PA * (26.7 * wt + 903 * htm) + add; }
    const PA = pal ? 1.16 : 1.0; return 135.3 - 30.8 * age + PA * (10.0 * wt + 934 * htm) + add;
  }
  if (sex === 1) { const PA = pal ? 1.11 : 1.0; return 662 - 9.53 * age + PA * (15.91 * wt + 539.6 * htm); }
  const PA = pal ? 1.12 : 1.0; return 354 - 6.91 * age + PA * (9.36 * wt + 726 * htm);
}

async function cycle([label, yr, suf, wvar]) {
  const D = parseXPT(await (await fetch(url(yr, suf, 'DEMO'))).arrayBuffer());
  const B = parseXPT(await (await fetch(url(yr, suf, 'BMX'))).arrayBuffer());
  const idx = new Map(); for (let i = 0; i < B.n; i++) idx.set(B.cols.SEQN[i], i);
  const g = {}; const add = (key, w, x) => { const a = g[key] || (g[key] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
    a[0] += 1; a[1] += w; a[2] += w * x.wt; a[3] += w * x.ht; a[4] += w * x.age;
    if (x.bmi > 0) { a[5] += w; a[6] += w * x.bmi; a[7] += w * x.bmi * x.wt; a[8] += w * x.bmi * x.bmi * x.wt; }
    a[9] += w * x.wt * x.wt; };
  const e = { all: [0, 0, 0, 0], ad2074: [0, 0, 0, 0], ad20p: [0, 0, 0, 0], kids: [0, 0, 0, 0] };
  const preg = D.cols.RIDEXPRG, mon = D.cols.RIDAGEMN || D.cols.RIDAGEEX, W = D.cols[wvar];
  for (let i = 0; i < D.n; i++) {
    const j = idx.get(D.cols.SEQN[i]); if (j === undefined) continue;
    const w = W[i]; if (!(w > 0)) continue;
    const sex = D.cols.RIAGENDR[i], age = D.cols.RIDAGEYR[i];
    const wt = B.cols.BMXWT[j], ht = B.cols.BMXHT[j], bmi = B.cols.BMXBMI[j];
    const pg = preg ? preg[i] === 1 : false;
    // energy requirement, all ages (pregnant women given the non-pregnant equation)
    const e0 = eer(sex, age, mon ? (age < 1 ? mon[i] : NaN) : NaN, wt, ht / 100, false);
    const e1 = eer(sex, age, mon ? (age < 1 ? mon[i] : NaN) : NaN, wt, ht / 100, true);
    if (e0 > 0) { const put = (k) => { e[k][0] += w; e[k][1] += w * e0; e[k][2] += w * e1; e[k][3] += 1; };
      put('all'); if (age >= 20 && age <= 74) put('ad2074'); if (age >= 20) put('ad20p'); if (age < 20) put('kids'); }
    if (age < 20 || !(wt > 0) || !(ht > 0)) continue;
    const x = { wt, ht, age, bmi };
    for (const set of ['2074', '20p']) {
      if (set === '2074' && age > 74) continue;
      add(`${sex}|${set}|incl`, w, x);
      if (!pg) add(`${sex}|${set}|excl`, w, x);
    }
  }
  const rows = [];
  for (const k of Object.keys(g).sort()) {
    const [sex, set, pr] = k.split('|'); const a = g[k];
    rows.push([label, sex, set, pr, a[0], a[1].toFixed(0), (a[2] / a[1]).toFixed(4), (a[3] / a[1]).toFixed(4), (a[4] / a[1]).toFixed(4),
      (a[6] / a[5]).toFixed(4), (a[7] / a[5]).toFixed(3), (a[8] / a[5]).toFixed(2), (a[9] / a[1]).toFixed(2)].join(','));
  }
  const erow = [label, ...['all', 'ad2074', 'ad20p', 'kids'].flatMap(k => [e[k][3], (e[k][1] / e[k][0]).toFixed(2), (e[k][2] / e[k][0]).toFixed(2), e[k][0].toFixed(0)])].join(',');
  return { rows, erow, nD: D.n, nB: B.n };
}

async function runAll() {
  let out = 'cycle,sex,ages,pregnant,n,sumw,wt_kg,ht_cm,age,bmi,bmi_x_wt,bmi2_x_wt,wt2\n';
  let eout = 'cycle,n_all,eer_sed_all,eer_low_all,sumw_all,n_2074,eer_sed_2074,eer_low_2074,sumw_2074,n_20p,eer_sed_20p,eer_low_20p,sumw_20p,n_kids,eer_sed_kids,eer_low_kids,sumw_kids\n';
  for (const c of CYCLES) { const r = await cycle(c); out += r.rows.join('\n') + '\n'; eout += r.erow + '\n'; }
  return out + '\n' + eout;
}

// ---- Self-reported energy intake (day-1 24-h recall), adults 20-74, by sex ----
const DIET = [
  ['1999-2000', '/Nchs/Data/Nhanes/Public/1999/DataFiles/DRXTOT.xpt', '1999', ''],
  ['2001-2002', '/Nchs/Data/Nhanes/Public/2001/DataFiles/DRXTOT_B.xpt', '2001', '_B'],
  ['2003-2004', '/Nchs/Data/Nhanes/Public/2003/DataFiles/DR1TOT_C.xpt', '2003', '_C'],
  ['2005-2006', '/Nchs/Data/Nhanes/Public/2005/DataFiles/DR1TOT_D.xpt', '2005', '_D'],
  ['2007-2008', '/Nchs/Data/Nhanes/Public/2007/DataFiles/DR1TOT_E.xpt', '2007', '_E'],
  ['2009-2010', '/Nchs/Data/Nhanes/Public/2009/DataFiles/DR1TOT_F.xpt', '2009', '_F'],
  ['2011-2012', '/Nchs/Data/Nhanes/Public/2011/DataFiles/DR1TOT_G.xpt', '2011', '_G'],
  ['2013-2014', '/Nchs/Data/Nhanes/Public/2013/DataFiles/DR1TOT_H.xpt', '2013', '_H'],
  ['2015-2016', '/Nchs/Data/Nhanes/Public/2015/DataFiles/DR1TOT_I.xpt', '2015', '_I'],
  ['2017-2018', '/Nchs/Data/Nhanes/Public/2017/DataFiles/DR1TOT_J.xpt', '2017', '_J'],
  ['2017-2020pre', '/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DR1TOT.xpt', '2017', 'P_'],
  ['2021-2023', '/Nchs/Data/Nhanes/Public/2021/DataFiles/DR1TOT_L.xpt', '2021', '_L'],
];
async function diet([label, f, yr, suf]) {
  const T = parseXPT(await (await fetch(f)).arrayBuffer());
  const D = parseXPT(await (await fetch(url(yr, suf, 'DEMO'))).arrayBuffer());
  const pick = (re) => Object.keys(T.cols).find(k => re.test(k));
  const kv = pick(/^DR(X|1)TKCAL$/), wv = pick(/^WTDR(D1|1D)(PP)?$/), sv = pick(/^DR(D|1)DRST[SZ]$/);
  const di = new Map(); for (let i = 0; i < D.n; i++) di.set(D.cols.SEQN[i], i);
  const acc = {};
  for (let i = 0; i < T.n; i++) {
    const j = di.get(T.cols.SEQN[i]); if (j === undefined) continue;
    const w = T.cols[wv][i], k = T.cols[kv][i], st = T.cols[sv][i];
    if (!(w > 0) || !(k >= 0) || st !== 1) continue;
    const age = D.cols.RIDAGEYR[j], sex = D.cols.RIAGENDR[j];
    if (age < 20 || age > 74) continue;
    const a = acc[sex] || (acc[sex] = [0, 0, 0]); a[0] += 1; a[1] += w; a[2] += w * k;
  }
  return [1, 2].map(s => [label, s, kv, wv, acc[s][0], acc[s][1].toFixed(0), (acc[s][2] / acc[s][1]).toFixed(2)].join(','));
}
async function runDiet() {
  let out = 'cycle,sex,kcal_var,weight_var,n,sumw,kcal_mean\n';
  for (const c of DIET) out += (await diet(c)).join('\n') + '\n';
  return out;
}
