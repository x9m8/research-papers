"""Economic allocation share of the hide at the slaughterhouse, monthly 2001-06 to 2025-12.
share = hide value per head / live value per head, live value = Nebraska fed-steer price ($/cwt live) x live weight.
Main live weight: federally inspected steer dressed weight / 0.63 (AMS drop-value dressing basis).
Alternatives: commercial all-cattle live weight; Texas/Oklahoma/New Mexico steer price."""
import json, numpy as np, pandas as pd
from common import RAW, RES
hide = pd.read_csv(f'{RES}/hide_monthly.csv', index_col=0).hide_usd; hide.index = pd.PeriodIndex(hide.index, freq='M')
m = pd.read_csv(f'{RAW}/Meat-Statistics.csv', low_memory=False); m = m[m.timeperiod_id.between(1, 12)]
def ms(com, att):
    x = m[(m.commodity_desc == com) & (m.attribute_desc == att)]
    return pd.Series(x.amount.values, index=pd.PeriodIndex.from_fields(year=x.year_id, month=x.timeperiod_id, freq='M')).sort_index()
steer_dw = ms('Steers', 'Federally inspected average dressed weight'); cattle_lw = ms('Cattle', 'Commercial average live weight')
cattle_dw = ms('Cattle', 'Federally inspected average dressed weight'); cattle_fi_lw = ms('Cattle', 'Federally inspected average live weight')
slaughter = ms('Cattle', 'Commercial slaughter')
p = pd.read_csv(f'{RAW}/LivestockPrices.csv')
def ps(geo, att):
    x = p[(p.geography_desc == geo) & (p.attribute_desc == att)]
    return pd.Series(x.amount.values, index=pd.PeriodIndex.from_fields(year=x.year_id, month=x.month_id, freq='M')).sort_index()
w = pd.read_csv(f'{RAW}/WholesalePrices.csv'); w = w[w.attribute_desc == 'Boxed beef cutout Choice 1-3, 600 - 900 pounds']
cut = pd.Series(w.amount.values, index=pd.PeriodIndex.from_fields(year=w.year_id, month=w.month_id, freq='M')).sort_index()
ne = ps('Nebraska', 'Steers 65-80 percent Choice'); tx = ps('Texas/Oklahoma/New Mexico', 'Steers 35-65 percent Choice')
D = pd.DataFrame(dict(cut=cut, hide=hide, ne=ne, tx=tx, steer_dw=steer_dw, cattle_lw=cattle_lw, cattle_dw=cattle_dw, cattle_fi_lw=cattle_fi_lw, slaughter=slaughter)).loc['2001-06':'2025-12']
D['steer_lw'] = D.steer_dw / 0.63
D['live_value'] = D['ne'] * D.steer_lw / 100
D['share'] = D.hide / D.live_value
D['share_cattle_lw'] = D.hide / (D['ne'] * D.cattle_lw / 100)
D['share_tx'] = D.hide / (D['tx'] * D.steer_lw / 100)
D['share_dress62'] = D.hide / (D['ne'] * D.steer_dw / 0.62 / 100); D['share_dress64'] = D.hide / (D['ne'] * D.steer_dw / 0.64 / 100)
D['share_output'] = D.hide / (D['cut'] * D.steer_dw / 100 + D.hide)
D['year'] = D.index.year
Y = D.groupby('year').agg(hide=('hide', 'mean'), ne=('ne', 'mean'), steer_lw=('steer_lw', 'mean'), live_value=('live_value', 'mean'),
                          share=('share', 'mean'), share_cattle_lw=('share_cattle_lw', 'mean'), share_tx=('share_tx', 'mean'),
                          share_dress62=('share_dress62', 'mean'), share_dress64=('share_dress64', 'mean'), share_output=('share_output', 'mean'), cut=('cut', 'mean'),
                          steer_dw=('steer_dw', 'mean'), slaughter=('slaughter', 'sum'), n=('hide', 'size'))
D.index = D.index.astype(str); D.to_csv(f'{RES}/allocation_monthly.csv'); Y.to_csv(f'{RES}/allocation_annual.csv')
pk = D.share.idxmax(); lo = D.share.idxmin()
out = dict(peak_month=pk, peak_share=float(D.share.max()), low_month=lo, low_share=float(D.share.min()),
           annual={int(y): {k: float(v) for k, v in r.items()} for y, r in Y.iterrows()})
json.dump(out, open(f'{RES}/allocation.json', 'w'), indent=1)
pd.set_option('display.width', 200)
print(Y.assign(**{c: 100 * Y[c] for c in Y.columns if c.startswith('share')}).round(2).to_string()); print(pk, D.share.max(), lo, D.share.min())
