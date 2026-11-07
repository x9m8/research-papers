"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
A1 = json.load(open(f'{RES}/a1_hpai_to_prices.json')); A2 = json.load(open(f'{RES}/a2_passthrough.json'))
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
r = A1['main']['avg_price_egg']; pk = max(r, key=lambda x: x['b'])
fs = A2['main']['cpi_fsr']; ls = A2['main']['cpi_lsr']
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Egg price spikes, no visible menu-price pass-through', fontsize=17, weight='bold', color=INK)
fig.text(0.04, 0.83, 'US monthly data, 2005-2026: HPAI layer losses, egg prices and restaurant CPI', fontsize=11, color=MUTED)
rows = [('Retail egg price per 10 million\nlayers confirmed (peak)', f"+{100*(2.718281828**(10*pk['b'])-1):.0f}%", f"{pk['h']} months after the detection month", BLUE),
        ('Full-service menu prices per\n10% rise in egg CPI', f"{10*fs['cum']+0:+.2f} pts".replace("-0.00","0.00").replace("+0.00","0.00"), f"95% CI {10*fs['cum_lo']:+.2f} to {10*fs['cum_hi']:+.2f}", ORANGE),
        ('Limited-service menu prices per\n10% rise in egg CPI', f"{10*ls['cum']+0:+.2f} pts".replace("-0.00","0.00").replace("+0.00","0.00"), f"95% CI {10*ls['cum_lo']:+.2f} to {10*ls['cum_hi']:+.2f}", GREEN)]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.58, k, fontsize=10, color=MUTED, va='bottom'); fig.text(x, 0.43, v, fontsize=24, weight='bold', color=col); fig.text(x, 0.36, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.2, 'Distributed-lag model with food-at-home and restaurant-wage controls; associations, not causal effects.', fontsize=10.5, color=INK)
fig.text(0.04, 0.14, 'National CPI cannot see individual restaurants, egg-heavy menus or contract prices.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · BLS and USDA APHIS public data · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
