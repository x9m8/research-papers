"""Monthly US butt-branded steer hide price ($/piece), 2001-06 to 2025-12: BLS PPI for cattle hides (WPU0419,
June 2001 = 100) scaled to dollars with one factor fitted to six USDA AMS report prices (geometric mean of
price/index ratios). Out-of-sample checks against published averages and secondary quotes."""
import json, io, numpy as np, pandas as pd
from common import RAW, DATA, RES
f = json.load(open(f'{RAW}/fred_20261020.json'))
ppi = pd.read_csv(io.StringIO(f['WPU0419'])); ppi.columns = ['date', 'ppi']; ppi['date'] = pd.to_datetime(ppi.date)
ppi['ym'] = ppi.date.dt.to_period('M'); P = ppi.set_index('ym').ppi
A = pd.read_csv(f'{DATA}/anchors.csv', parse_dates=['date']); A['ym'] = A.date.dt.to_period('M'); A['ppi'] = A.ym.map(P)
cal = A[A.role == 'calibration'].copy(); cal['ratio'] = cal.price / cal.ppi
k = float(np.exp(np.log(cal.ratio).mean()))
cal['fitted'] = k * cal.ppi; cal['err_pct'] = 100 * (cal.fitted / cal.price - 1)
# leave-one-out
loo = []
for i in cal.index:
    kk = float(np.exp(np.log(cal.drop(i).ratio).mean())); loo.append(100 * (kk * cal.loc[i, 'ppi'] / cal.loc[i, 'price'] - 1))
cal['loo_err_pct'] = loo
hide = (k * P).rename('hide_usd')
def avg(a, b): return float(hide[pd.Period(a, 'M'):pd.Period(b, 'M')].mean())
val = A[A.role != 'calibration'].copy()
val['fitted'] = [avg('2018-01', '2018-12') if r == 'validation_annual2018' else avg('2019-01', '2019-06') if r == 'validation_h12019'
                 else avg('2013-01', '2017-12') if r == 'validation_avg1317' else float(hide[m]) for r, m in zip(val.role, val.ym)]
val['err_pct'] = 100 * (val.fitted / val.price - 1)
out = dict(k=k, k_range=[float(cal.ratio.min()), float(cal.ratio.max())],
           cal=cal[['date', 'price', 'ppi', 'ratio', 'fitted', 'err_pct', 'loo_err_pct']].assign(date=cal.date.astype(str)).to_dict('records'),
           val=val[['date', 'price', 'kind', 'source', 'fitted', 'err_pct']].assign(date=val.date.astype(str)).to_dict('records'),
           val_mape=float(val.err_pct.abs().mean()), val_median_abs=float(val.err_pct.abs().median()),
           cal_rmse_log=float(np.sqrt((np.log(cal.fitted / cal.price) ** 2).mean())))
hide.index = hide.index.astype(str); hide.to_csv(f'{RES}/hide_monthly.csv')
json.dump(out, open(f'{RES}/hide_calibration.json', 'w'), indent=1, default=float)
print(f'k={k:.4f}'); print(cal[['date', 'price', 'ppi', 'fitted', 'err_pct', 'loo_err_pct']].round(2).to_string())
print(val[['date', 'price', 'fitted', 'err_pct', 'source']].round(1).to_string()); print('val MAPE', round(out['val_mape'], 1))
