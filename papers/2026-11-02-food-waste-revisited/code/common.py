"""Shared paths, loaders, Hall et al. (2009) model parameters and the closed-form intake/waste calculation."""
import os, io, json, re
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
RAW = os.path.join(ROOT, 'data', 'raw'); DER = os.path.join(ROOT, 'data', 'derived')
RES = os.path.join(ROOT, 'results'); FIG = os.path.join(ROOT, 'figures')
for d in (DER, RES, FIG): os.makedirs(d, exist_ok=True)

# ---- Hall et al. (2009) parameters. Nominal values as used in the text (gamma_F = 3.2 kcal/kg/d, eq. 14 gives 9,100 and 22);
# Table 1 lists gamma_F = 3.6 +/- 2. Means and SDs for the Monte Carlo are Table 1.
NOMINAL = dict(gF=3.2, gFFM=22.0, delta=7.0, beta=0.24, etaFFM=230.0, etaF=180.0, C=10.4, I0=2100.0, rhoF=9400.0, rhoFFM=1800.0)
TABLE1 = dict(gFFM=(22, 4), gF=(3.6, 2), delta=(7, 4), beta=(0.24, 0.1), etaFFM=(230, 100), etaF=(180, 20), C=(10.4, 5), I0=(2100, 100))
F0_HALL = 19.1      # kg, Hall et al. (2009) eq. 10
P_W = 0.525         # proportion of women, Hall et al. (2009)
KCAL_PER_BTU = 0.252; BTU_PER_BBL = 5.8e6   # EIA crude-oil heat content, 5.8 million Btu per barrel
FOSSIL_PER_FOOD = 3.0; AG_SHARE_WATER = 0.70  # Hall et al. (2009) Discussion: 3 kcal fossil per kcal food; agriculture ~70% of freshwater


def coefs(p, F0):
    """Return (C_dyn [kcal/kg], C_static [kcal/kg/d]) of Hall's eq. 13 with delta held constant (delta = delta0)."""
    a = p['C'] / F0
    cdyn = (p['etaF'] + p['rhoF'] + a * (p['etaFFM'] + p['rhoFFM'])) / ((1 + a) * (1 - p['beta']))
    csta = ((p['gF'] + a * p['gFFM']) / (1 + a) + p['delta']) / (1 - p['beta'])
    return cdyn, csta


def bw_path(points, years):
    """Piecewise-linear mean body weight through survey points [(t, BW)], evaluated at mid-year of each calendar year,
    and its slope (kg/yr). Beyond the last point the last segment's slope is used to extrapolate (flagged by caller)."""
    t = np.array([p[0] for p in points], float); w = np.array([p[1] for p in points], float)
    yy = np.asarray(years, float)
    bw = np.interp(yy, t, w)
    slope = np.empty_like(yy)
    for i, y in enumerate(yy):
        k = np.searchsorted(t, y, side='right') - 1; k = min(max(k, 0), len(t) - 2)
        slope[i] = (w[k + 1] - w[k]) / (t[k + 1] - t[k])
    after = yy > t[-1]
    bw[after] = w[-1] + slope[after] * (yy[after] - t[-1])
    return bw, slope


def intake(points, years, p, F0, base_year=1974.0, delta_path=None):
    """Hall eq. 13: mean intake I(t) = I0 + dI(t). BW0 is the body weight at base_year (assumed energy balance).
    delta_path: optional array of delta(t) (kcal/kg/d) to allow a change in physical activity (default constant)."""
    bw, slope = bw_path(points, years)
    bw0 = float(np.interp(base_year, [q[0] for q in points], [q[1] for q in points]))
    cdyn, csta = coefs(p, F0)
    dyn = cdyn * slope / 365.25
    a = p['C'] / F0
    if delta_path is None:
        sta = csta * (bw - bw0)
    else:
        sta = (((p['gF'] + a * p['gFFM']) / (1 + a)) * (bw - bw0) + delta_path * bw - p['delta'] * bw0) / (1 - p['beta'])
    dI = dyn + sta
    return dict(bw=bw, slope=slope, bw0=bw0, dyn=dyn, sta=sta, dI=dI, I=p['I0'] + dI)


def jackson_fat(sex, m_bw, m_bmibw, m_bmi2bw):
    """Population-mean fat mass (kg) from Jackson et al. (2002) as printed in Hall et al. (2009) eq. 10."""
    if sex == 1: return (3.76 * m_bmibw - 0.04 * m_bmi2bw - 47.80 * m_bw) / 100
    return (4.35 * m_bmibw - 0.05 * m_bmi2bw - 46.24 * m_bw) / 100


# ---------------- loaders ----------------
def load_fao():
    """FAOSTAT food supply (kcal/capita/day) and population for the USA: old methodology (FBSH, 1961-2013) and new (FBS, 2010-)."""
    txt = open(os.path.join(RAW, 'fao', 'fao_usa_fbsh_fbs.txt'), encoding='latin1').read()
    blocks = [b for b in txt.strip().split('\n\n')]
    out = {}
    for b in blocks:
        lines = b.strip().split('\n'); name = 'FBSH' if lines[0].startswith('# FBSH') else 'FBS'
        df = pd.read_csv(io.StringIO('\n'.join(lines[1:]).replace('E",', 'E')))
        out[name] = df.set_index('year')
    return out


def load_nhanes():
    txt = open(os.path.join(RAW, 'nhanes', 'nhanes_continuous_aggregates.csv')).read().strip().split('\n\n')
    a = pd.read_csv(io.StringIO(txt[0])); e = pd.read_csv(io.StringIO(txt[1]))
    return a, e


def load_ogden():
    return pd.read_csv(os.path.join(RAW, 'nhanes', 'ogden2004_ad347_adult_means.csv'))


def load_diet():
    return pd.read_csv(os.path.join(RAW, 'nhanes', 'nhanes_diet_kcal_aggregates.csv'))


def load_lafa():
    df = pd.read_csv(os.path.join(RAW, 'other', 'ers_lafa_calories.csv'), skiprows=1)
    df = df[df['Year'].astype(str).str.match(r'^\d{4}')].copy()
    df['year'] = df['Year'].astype(str).str[:4].astype(int)
    df['total'] = pd.to_numeric(df['Total'].astype(str).str.replace(',', ''), errors='coerce')
    return df.set_index('year')['total']


def load_epa():
    lines = open(os.path.join(RAW, 'other', 'epa_food_msw.txt')).read().strip().split('\n')
    yrs = [int(x) for x in lines[1].split('|')[1:]]
    gen = [float(x.replace(',', '')) for x in lines[2].split('|')[1:]]
    return pd.Series(gen, index=yrs, name='generation_1000_tons')


def load_eia():
    return pd.read_csv(os.path.join(RAW, 'other', 'eia_product_supplied.csv'), comment='#').set_index('year')['kbd']


def load_digitized():
    return pd.read_csv(os.path.join(RAW, 'other', 'hall2009_fig1_digitized.csv'), comment='#')


def dump(obj, name):
    def conv(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return None if np.isnan(o) else float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, pd.Series): return o.to_dict()
        raise TypeError(type(o))
    json.dump(obj, open(os.path.join(RES, name), 'w'), indent=1, default=conv)


def load(name): return json.load(open(os.path.join(RES, name)))
