"""Analysis 1: layer-flock losses (APHIS) -> producer (PPI) and retail egg prices, 2022-02 to 2026-09. Local projections.
y_{t+h} - y_{t-1} = a_h + b_h * L_t + c1 L_{t-1} + c2 L_{t-2} + d1 (y_{t-1}-y_{t-2}) + e ; HAC (Newey-West, maxlags = h+3). L = millions of commercial table-egg layers confirmed in month t."""
import json, numpy as np, pandas as pd, statsmodels.api as sm
from common import *
d = load_monthly(); L, n = monthly_layers()
YS = {'ppi_egg_large': 'PPI, large eggs (producer)', 'ppi_egg_all': 'PPI, chicken eggs (producer)', 'cpi_egg': 'CPI, eggs (retail)', 'avg_price_egg': 'Avg price, Grade A large (retail)'}
H = 8
def lp(y, shock_lags=2, h_max=H, spec='main'):
    ly = np.log(d[y]); out = []
    full = pd.period_range('2021-10', '2026-09', freq='M')
    Lf = L.reindex(full, fill_value=0.0)  # pre-2022-02 months set to 0 only for lag construction (sample starts at 2022-02; see manuscript)
    for h in range(0, h_max + 1):
        X = pd.DataFrame({'L0': Lf})
        for k in range(1, shock_lags + 1): X[f'L{k}'] = Lf.shift(k)
        if spec != 'nolagy': X['dy1'] = (ly - ly.shift(1)).shift(1).reindex(full)
        Y = (ly.shift(-h) - ly.shift(1)).reindex(full)
        df = pd.concat([Y.rename('Y'), X], axis=1).loc['2022-02':'2026-09'].dropna()
        m = sm.OLS(df['Y'], sm.add_constant(df.drop(columns='Y'))).fit(cov_type='HAC', cov_kwds={'maxlags': h + 3})
        b, se = m.params['L0'], m.bse['L0']
        out.append({'h': h, 'b': b, 'se': se, 'lo': b - 1.96 * se, 'hi': b + 1.96 * se, 'p': float(m.pvalues['L0']), 'n': int(m.nobs),
                    'b_pct_per10M': 100 * (np.exp(10 * b) - 1)})
    return out
res = {'names': YS, 'main': {y: lp(y) for y in YS}, 'nolagy': {y: lp(y, spec='nolagy') for y in YS}, 'lags4': {y: lp(y, shock_lags=4) for y in YS}}
# cross-correlations of monthly layers with monthly log price change
cc = {}
for y in YS:
    dy = np.log(d[y]).diff().reindex(L.index)
    cc[y] = {str(k): float(L.corr(dy.shift(-k))) for k in range(-3, 7)}
res['xcorr'] = cc
# cumulative-stock regression: log price level on trailing 6-month layer losses
stock = {}
for y in YS:
    ly = np.log(d[y]).reindex(L.index); S = L.rolling(6).sum()
    df = pd.concat([ly.rename('y'), S.rename('S')], axis=1).dropna()
    m = sm.OLS(df['y'], sm.add_constant(df['S'])).fit(cov_type='HAC', cov_kwds={'maxlags': 6})
    stock[y] = {'b': float(m.params['S']), 'se': float(m.bse['S']), 'r2': float(m.rsquared), 'n': int(m.nobs)}
res['stock6'] = stock
res['layers'] = {'total_M': float(L.sum()), 'n_flocks': int(n.sum()), 'months_with_detection': int((L > 0).sum()), 'months': int(len(L)),
                 'peak_month': str(L.idxmax()), 'peak_M': float(L.max()),
                 'by_event': {'2022': float(L['2022-02':'2022-12'].sum()), '2023': float(L['2023-01':'2023-12'].sum()), '2024': float(L['2024-01':'2024-12'].sum()),
                              '2025': float(L['2025-01':'2025-12'].sum()), '2026_to_sep': float(L['2026-01':'2026-09'].sum()),
                              'dec2024_feb2025': float(L['2024-12':'2025-02'].sum()), 'nov2023_jan2024': float(L['2023-11':'2024-01'].sum()), 'mar_apr2022': float(L['2022-03':'2022-04'].sum())}}
# peaks of retail price and PPI around waves
pk = {}
for y in ['avg_price_egg', 'cpi_egg', 'ppi_egg_large']:
    for lab, a, b in [('wave2022', '2022-02', '2023-06'), ('wave2024_25', '2024-09', '2025-12'), ('wave2025_26', '2025-11', '2026-09')]:
        s = d[y][a:b]; pk[f'{y}_{lab}'] = {'max': float(s.max()), 'month': str(s.idxmax()), 'min': float(s.min()), 'min_month': str(s.idxmin())}
res['peaks'] = pk
res['retail_levels'] = {k: float(d['avg_price_egg'][k]) for k in ['2022-01', '2022-12', '2023-01', '2024-09', '2025-02', '2025-03', '2025-09', '2025-11', '2026-09']}
json.dump(res, open(f'{RES}/a1_hpai_to_prices.json', 'w'), indent=1)
for y in YS:
    print(y); [print(' h', r['h'], f"b={r['b']:.4f} se={r['se']:.4f} p={r['p']:.3f} n={r['n']} pct10M={r['b_pct_per10M']:.1f}") for r in res['main'][y]]
print(res['layers']); print(res['stock6']); print(res['retail_levels'])
