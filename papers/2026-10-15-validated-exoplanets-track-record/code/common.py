"""Shared paths and readers. Raw inputs (not redistributed) are queried from:
  NASA Exoplanet Archive TAP (https://exoplanetarchive.ipac.caltech.edu/TAP/sync), tables pscomppars, ps,
    cumulative, keplernames, k2pandc, toi; snapshot 15 October 2026 (see README for the exact ADQL queries);
  VizieR (https://vizier.cds.unistra.fr) catalogues of the validation papers (IDs listed in BATCH_VIZIER below).
Set RAW to the folder holding the CSV/TSV snapshots."""
import os, re, pandas as pd, numpy as np
RAW = os.environ.get('P3_RAW', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw'))
RES = os.path.join(os.path.dirname(__file__), '..', 'results')
FIG = os.path.join(os.path.dirname(__file__), '..', 'figures')

def nea(name):
    d = pd.read_csv(os.path.join(RAW, name + '.csv'), low_memory=False)
    for c in ('disc_refname', 'pl_refname', 'disp_refname'):
        if c in d:
            s = d[c].astype(str)
            d[c.replace('refname', 'ref')] = s.str.split('|').str[0].str.strip().str.replace('&aacute;', 'a').str.replace('&eacute;', 'e').str.replace('&iacute;', 'i').str.replace('&amp;', '&')
            d[c.replace('refname', 'bib')] = s.str.split('|').str[1]
    return d

def vizier(cat):
    """Read a VizieR ASU-TSV dump (header line, units line, dashes line, then rows)."""
    f = os.path.join(RAW, 'vizier', cat.replace('/', '_') + '.tsv')
    L = [l for l in open(f, encoding='utf-8').read().split('\n') if l and not l.startswith('#')]
    hdr = L[0].split('\t')
    rows = [x.split('\t') for x in L[3:]]
    return pd.DataFrame(rows, columns=hdr).apply(lambda s: s.str.strip())

def norm_k2(s):
    """'K2-42b', 'K2- 156 b', 'K2-42 b' -> 'K2-42 b'."""
    if not isinstance(s, str) or not s.strip(): return None
    m = re.match(r'K2-\s*(\d+)\s*([a-z])', s.strip())
    return f'K2-{m.group(1)} {m.group(2)}' if m else None

def mission(fac):
    if fac == 'Kepler': return 'Kepler'
    if fac == 'K2': return 'K2'
    if isinstance(fac, str) and 'TESS' in fac: return 'TESS'
    return 'Other'
