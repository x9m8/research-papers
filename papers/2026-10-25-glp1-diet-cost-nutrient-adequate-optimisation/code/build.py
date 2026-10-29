"""Link FNDDS 2017-2018 nutrient values to ERS PP-NAP 2017/2018 national average prices; inflate to 2026 dollars with the ERS food-at-home CPI."""
import json, numpy as np, pandas as pd
from common import *
n = pd.read_excel(f'{RAW}/FNDDS1718_nutrients.xlsx', header=1)
p = pd.read_csv(f'{RAW}/ppnap/pp_national_average_prices_csv.csv', encoding='cp1252')
p = p[p.year == '2017/2018'][['food_code', 'price_100gm', 'method_description']].rename(columns={'food_code': 'Food code'})
p['Food code'] = p['Food code'].astype(int)
d = n.merge(p, on='Food code', how='inner')
# CPI food at home, annual average % change (ERS)
c = pd.read_csv(f'{RAW}/CPI_annual_pct.csv', encoding='utf-8-sig'); c.columns = ['item', 'year', 'pct']
fah = c[c.item == 'Food at home'].astype({'year': int}).set_index('year').pct
idx = {2016: 100.0}
for y in range(2017, 2026): idx[y] = idx[y - 1] * (1 + fah[y] / 100)
f = pd.read_csv(f'{RAW}/CPI_hist_forecast.csv', encoding='utf-8-sig'); f.columns = ['item', 'm', 'yf', 'yb', 'attr', 'pct']
g = f[(f.item == 'Food at home') & (f.yf == 2026) & (f.yb == 2026)]; latest = g.m.max(); g = g[g.m == latest].set_index('attr').pct
fac_2025 = idx[2025] / ((idx[2017] + idx[2018]) / 2)
fac = {k: fac_2025 * (1 + g[a] / 100) for k, a in [('mid', 'Midpoint of forecast interval'), ('lo', 'Lower bound of forecast interval'), ('hi', 'Upper bound of forecast interval')]}
d['price_100g_2026'] = d.price_100gm * fac['mid']
d.to_csv(f'{RES}/foods_priced.csv', index=False)
json.dump(dict(n_fndds=len(n), n_ppnap_1718=len(p), n_linked=len(d), cpi_food_at_home_pct=fah.loc[2017:2025].to_dict(), factor_1718_to_2025=fac_2025,
               forecast_2026_month=int(latest), forecast_2026_pct=g.to_dict(), factor_to_2026=fac), open(f'{RES}/build.json', 'w'), indent=1)
print(len(n), len(p), len(d), fac_2025, fac)
