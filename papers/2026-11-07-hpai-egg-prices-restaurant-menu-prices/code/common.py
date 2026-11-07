"""Shared paths and data loaders for paper 23 (egg prices, HPAI and restaurant menu prices)."""
import os, hashlib
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
RAW = os.path.join(ROOT, 'data', 'raw'); DERIVED = os.path.join(ROOT, 'data', 'derived'); RES = os.path.join(ROOT, 'results'); FIG = os.path.join(ROOT, 'figures')
IDX = pd.period_range('2005-01', '2026-09', freq='M')
NAMES = {  # series id -> short name
 'CUUR0000SEFH': 'cpi_egg', 'CUUR0000SAF11': 'cpi_fah', 'CUUR0000SEFV': 'cpi_fafh', 'CUUR0000SEFV01': 'cpi_fsr', 'CUUR0000SEFV02': 'cpi_lsr',
 'CUURS12ASEFV': 'ny_fafh', 'CUURS12ASAF11': 'ny_fah', 'CUUR0000SA0': 'cpi_all', 'CUURS12ASA0': 'ny_all',
 'CUSR0000SEFH': 'sa_egg', 'CUSR0000SAF11': 'sa_fah', 'CUSR0000SEFV': 'sa_fafh', 'CUSR0000SEFV01': 'sa_fsr',
 'APU0000708111': 'avg_price_egg', 'WPU0171': 'ppi_egg_all', 'WPU01710703': 'ppi_egg_large',
 'CES7072200008': 'ahe_food_prod', 'CES7072200003': 'ahe_food_all', 'CES0500000003': 'ahe_private'}
def _parse(path):
    out = {}
    for line in open(path).read().split('\n'):
        sid, vals = line.split(':'); v = [float(x) if x != '' else np.nan for x in vals.split(',')]
        assert len(v) == len(IDX), sid
        out[NAMES[sid]] = v
    return out
def load_monthly():
    d = {}; d.update(_parse(f'{RAW}/bls_wide.txt')); d.update(_parse(f'{RAW}/bls_ppi_wide.txt'))
    return pd.DataFrame(d, index=IDX)
def monthly_layers():
    """Commercial table-egg layer birds confirmed per month (millions) and flock count, 2022-02 to 2026-09; months
    without a detection = 0. This is a derived, aggregate series (data/derived/aphis_table_egg_layer_losses_monthly.csv),
    computed from the public USDA APHIS HPAI detections dashboard (see data/SOURCES.md for the URL and retrieval date).
    The underlying per-detection extract (dates, counties, flock IDs) is not redistributed in this package; see
    data/SOURCES.md for why, and for how to reproduce this file yourself from the live dashboard."""
    df = pd.read_csv(f'{DERIVED}/aphis_table_egg_layer_losses_monthly.csv')
    idx = pd.PeriodIndex(df['month'], freq='M')
    s = pd.Series(df['commercial_table_egg_layer_birds_millions'].values, index=idx)
    n = pd.Series(df['commercial_table_egg_layer_flocks'].values, index=idx)
    full = pd.period_range('2022-02', '2026-09', freq='M')
    return s.reindex(full, fill_value=0.0), n.reindex(full, fill_value=0)
def sha256(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
