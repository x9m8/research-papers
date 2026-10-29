"""Shared paths, variable lists and small helpers."""
import os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
RAW = os.path.join(ROOT, 'data', 'raw'); DER = os.path.join(ROOT, 'data', 'derived')
RES = os.path.join(ROOT, 'results'); FIG = os.path.join(ROOT, 'figures')
for d in (DER, RES, FIG): os.makedirs(d, exist_ok=True)

RFEI = {'trad': 'Traditional RFEI', 'e1': 'Expanded RFEI #1 (supercenters unhealthy)', 'e2': 'Expanded RFEI #2 (supercenters healthy)'}
# Control set that reproduces the published Table 6 (R2, N, control coefficients and their state-clustered SEs):
# the Table 9 / Table A4 covariates. The notes to Tables 6-8 list "number of people over 65" but not % bachelor's;
# that literal set (CTRL_NOTE) is run as a variant.
CTRL = ['lila', 'recfac', 'natamen', 'milksoda', 'pct_black', 'pct_hisp', 'povrate', 'sqmi', 'bach_only']
CTRL_NOTE = ['lila', 'recfac', 'natamen', 'milksoda', 'pct_black', 'pct_hisp', 'pop65', 'povrate', 'sqmi']
TARGET = {  # published values, read from the MDPI HTML and PDF (both identical), see manuscript Table 1
    'ols': {'e1': (0.120, 0.0579, 3069, 0.559), 'e2': (0.115, 0.0499, 3069, 0.560), 'trad': (0.125, 0.0443, 3055, 0.560)},
    'fs_F': {'e1': 7.87, 'e2': 7.44, 'trad': 15.66},
    'iv': {'e1': (1.510, 0.434, 3069), 'e2': (1.277, 0.383, 3069), 'trad': (2.604, 1.076, 3055)},
    'iv_strat': {'commute<80': (2.452, 1.218, 1230), 'commute>80': (4.016, 3.946, 1825), 'gini<0.41': (2.737, 1.277, 2442), 'gini>0.41': (1.564, 0.686, 613)},
    'ols_A4': {'e1': (0.118, 0.0582), 'e2': (0.114, 0.0503), 'trad': (0.123, 0.0450)},
    'iv_A5': {'e1': (1.165, 0.350), 'e2': (0.993, 0.317), 'trad': (2.074, 0.864)},
}

def dump(obj, name):
    def conv(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return None if np.isnan(o) else float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        raise TypeError(type(o))
    json.dump(obj, open(os.path.join(RES, name), 'w'), indent=1, default=conv)

def load(name): return json.load(open(os.path.join(RES, name)))
