"""Three figures from results/*.json -> figures/fig{1,2,3}_*.{png,pdf}, 300 dpi."""
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from common import RESULTS, FIG
from style import BLUE, ORANGE, GREEN, INK, MUTED, WATERBODY_COLOR, save

desc = json.load(open(f'{RESULTS}/descriptives.json'))
rain = json.load(open(f'{RESULTS}/rainfall.json'))
closures = json.load(open(f'{RESULTS}/closures.json'))

# --- Figure 1: annual exceedance rate, 2015-2025 -----------------------------------
by_year = sorted(desc['by_year'], key=lambda r: r['year'])
years = [r['year'] for r in by_year]
rates = [100 * r['rate'] for r in by_year]
ns = [r['n'] for r in by_year]
overall = 100 * desc['exceedance_rate']

fig, ax = plt.subplots(figsize=(6.0, 3.6))
ax.bar(years, rates, color=BLUE, width=0.65)
ax.axhline(overall, color=MUTED, linewidth=1, linestyle='--')
ax.text(years[-1] + 0.6, overall, f'{overall:.1f}% overall', fontsize=7.5, color=MUTED, va='center')
for x, r, n in zip(years, rates, ns):
    ax.text(x, r + 0.35, f'n={n}', fontsize=6, color=MUTED, ha='center', rotation=90, va='bottom')
ax.set_ylabel('Enterococcus exceedance rate (%)')
ax.set_xticks(years)
ax.set_xticklabels(years, rotation=45, ha='right')
ax.set_ylim(0, max(rates) * 1.35)
ax.set_title('Enterococcus single-sample exceedances by year\nNY State Park beaches, Long Island, 2015–2025', fontsize=9.5)
save(fig, 'fig1_annual_exceedance', FIG)

# --- Figure 2: exceedance rate by beach, colored by waterbody ----------------------
by_beach = sorted(desc['by_beach'], key=lambda r: r['rate'])
names = [r['state_park_beach'] for r in by_beach]
rates_b = [100 * r['rate'] for r in by_beach]
cols = [WATERBODY_COLOR[r['waterbody']] for r in by_beach]
ns_b = [r['n'] for r in by_beach]

fig, ax = plt.subplots(figsize=(6.2, 5.2))
y = range(len(names))
ax.barh(list(y), rates_b, color=cols, height=0.68)
for yi, r, n in zip(y, rates_b, ns_b):
    ax.text(r + 0.25, yi, f'n={n}', fontsize=6, color=MUTED, va='center')
ax.set_yticks(list(y))
ax.set_yticklabels(names, fontsize=7.3)
ax.set_xlabel('Enterococcus exceedance rate (%), 2015–2025')
ax.set_title('Exceedance rate by beach station', fontsize=9.5)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in WATERBODY_COLOR.values()]
ax.legend(handles, list(WATERBODY_COLOR.keys()), loc='lower right', fontsize=7.3)
save(fig, 'fig2_by_beach', FIG)

# --- Figure 3: exceedance rate by prior-48h rainfall bucket ------------------------
buckets = rain['exceedance_by_rain_bucket']
order = ['0 mm', '0-10 mm', '10-25 mm', '>25 mm']
buckets = sorted(buckets, key=lambda r: order.index(r['rain_bucket']))
labels = [r['rain_bucket'] for r in buckets]
rates_r = [100 * r['rate'] for r in buckets]
ns_r = [r['n'] for r in buckets]

fig, ax = plt.subplots(figsize=(5.4, 3.6))
ax.bar(labels, rates_r, color=ORANGE, width=0.6)
for i, (r, n) in enumerate(zip(rates_r, ns_r)):
    ax.text(i, r + 0.3, f'n={n}', fontsize=7, color=MUTED, ha='center')
ax.set_ylabel('Enterococcus exceedance rate (%)')
ax.set_xlabel('Rainfall at the assigned station in the 48 hours before sampling')
ax.set_title('Exceedance rate rises with recent rainfall\nbeach fixed-effects odds ratio %.2f per cm (95%% CI %.2f–%.2f)' % (
    rain['main_48h']['odds_ratio_per_unit'], rain['main_48h']['or_ci95_cluster'][0], rain['main_48h']['or_ci95_cluster'][1]),
    fontsize=9)
save(fig, 'fig3_rainfall', FIG)

print('figures written')
