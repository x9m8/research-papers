"""Upper bounds on menu-price effects implied by the 95% CIs for the two observed egg-price waves (12-month egg CPI changes at peak)."""
import json, math
from common import RES
A2 = json.load(open(f'{RES}/a2_passthrough.json')); out = {}
for lab in ['wave1', 'wave2']:
    e = A2['desc'][lab]['cpi_egg']; x = math.log(1 + e / 100)
    out[lab] = {'peak_month': A2['desc'][lab]['peak_month'], 'egg_yoy_pct': e, 'egg_log_change': x}
    for y in ['cpi_fsr', 'cpi_lsr', 'cpi_fafh']:
        m = A2['main'][y]; out[lab][y] = {'point_pct': 100 * m['cum'] * x, 'lo_pct': 100 * m['cum_lo'] * x, 'hi_pct': 100 * m['cum_hi'] * x}
json.dump(out, open(f'{RES}/a3_bounds.json', 'w'), indent=1); print(json.dumps(out, indent=1))
