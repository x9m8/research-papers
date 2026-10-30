"""Figures 1-3 from results/*.json."""
import json
import numpy as np, pandas as pd
from style import *
from common import RES, FIG
C = json.load(open(f'{RES}/composition.json')); P = json.load(open(f'{RES}/prices.json'))
d = pd.read_pickle(f'{RES}/../data/derived/products.pkl')
short = lambda c: (c.replace('Snack, Energy & Granola Bars', 'Snack & granola bars').replace('Energy, Protein & Muscle Recovery Drinks', 'Protein & recovery drinks')
                   .replace('Popcorn, Peanuts, Seeds & Related Snacks', 'Popcorn, nuts & seeds').replace('Meat/Poultry/Other Animals - Prepared/Processed', 'Meat, prepared/processed')
                   .replace('Fruit & Vegetable Juice, Nectars & Fruit Drinks', 'Juice & fruit drinks').replace("Frozen Appetizers & Hors D'oeuvres", 'Frozen appetizers')
                   .replace('Cake, Cookie & Cupcake Mixes', 'Cake & cookie mixes').replace('Cakes, Cupcakes, Snack Cakes', 'Snack cakes'))
top = sorted(C['category_table'], key=lambda c: -C['category_table'][c]['n_E2'])[:16]

# ---- Figure 1: label protein per serving among protein-named products vs others, by category ----
e = d[d.prot_serv.notna()]
rows = []
for c in top:
    g = e[e.branded_food_category == c]; a = g[g.E2]; b = g[~g.E2]
    rows.append((c, (a.prot_serv < 4.5).mean(), ((a.prot_serv >= 4.5) & (a.prot_serv < 9.5)).mean(), (a.prot_serv >= 9.5).mean(), (b.prot_serv >= 9.5).mean(), len(a)))
rows = rows[::-1]
fig, ax = plt.subplots(figsize=(6.6, 5.2))
y = np.arange(len(rows))
l = [r[1] for r in rows]; m = [r[2] for r in rows]; h = [r[3] for r in rows]
ax.barh(y, l, color=LIGHT, label='< 5 g'); ax.barh(y, m, left=l, color=YELLOW, label='5–9 g ("good source" range)')
ax.barh(y, h, left=np.add(l, m), color=BLUE, label='≥ 10 g ("high" range)')
ax.scatter([r[4] for r in rows], y, marker='D', s=16, color=INK, zorder=3, label='Other products in category: share ≥ 10 g')
ax.set_yticks(y, [f'{short(r[0])} (n={r[5]})' for r in rows]); ax.set_xlim(0, 1)
ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0)); ax.set_xlabel('Share of protein-named products, by label protein per labelled serving')
ax.legend(loc='upper center', bbox_to_anchor=(0.4, -0.12), ncol=2, fontsize=7.5); ax.grid(axis='y', visible=False)
save(fig, 'fig1_eligibility', FIG)

# ---- Figure 2: category medians, protein-named vs other products ----
panels = [('protein', 'Protein,\ng per 100 g'), ('asug_per100k', 'Added sugars,\ng per 100 kcal'), ('na_per100k', 'Sodium,\nmg per 100 kcal'), ('upf_classes', 'Marker classes in\ningredients, n of 9')]
fig, axs = plt.subplots(1, 4, figsize=(7.4, 5.0), sharey=True)
cats = top[::-1]; y = np.arange(len(cats))
for ax, (k, lab) in zip(axs, panels):
    pc = C['C1_E2'][k]['per_category']
    for i, c in enumerate(cats):
        if c not in pc: continue
        a, b = pc[c]['exp'], pc[c]['cmp']
        ax.plot([b, a], [i, i], color=LIGHT, lw=1.2, zorder=1)
        ax.scatter(a, i, color=ORANGE, s=16, zorder=2); ax.scatter(b, i, facecolor='none', edgecolor=INK, linewidth=0.9, s=22, zorder=3)
    ax.set_title(lab, fontsize=8); ax.grid(axis='y', visible=False)
axs[0].set_yticks(y, [short(c) for c in cats], fontsize=7)
axs[0].scatter([], [], color=ORANGE, s=16, label='Protein-named (median)'); axs[0].scatter([], [], facecolor='none', edgecolor=INK, linewidth=0.9, s=22, label='Other products in category (median)')
fig.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.55, -0.02), fontsize=7.5); fig.subplots_adjust(bottom=0.14, wspace=0.12)
save(fig, 'fig2_composition', FIG)

# ---- Figure 3: whole-food protein cost and breakeven package prices ----
W = pd.DataFrame(P['whole_foods']).sort_values('usd_per_10g_protein')
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 4.0), gridspec_kw={'width_ratios': [1, 1.25]})
lab = {'eggs': 'Eggs', 'milk_whole': 'Milk, whole', 'milk_lowfat': 'Milk, low-fat', 'beans_dry': 'Dry beans', 'chicken_breast': 'Chicken breast', 'ground_beef': 'Ground beef',
       'ground_beef_lean': 'Ground beef, lean', 'cheddar': 'Cheddar', 'yogurt': 'Yogurt', 'bread_white': 'White bread', 'rice_white': 'White rice'}
yy = np.arange(len(W))
a1.barh(yy, W.usd_per_10g_protein, color=[BLUE if b else LIGHT for b in W.benchmark])
a1.errorbar(W.usd_per_10g_protein, yy, xerr=[W.usd_per_10g_protein - W.usd_per_10g_protein_min, W.usd_per_10g_protein_max - W.usd_per_10g_protein], fmt='none', ecolor=MUTED, lw=0.8)
a1.set_yticks(yy, [lab[k] for k in W.key]); a1.set_xlabel('US$ per 10 g protein (Oct 2025–Sep 2026)'); a1.grid(axis='y', visible=False)
a1.set_title('Whole foods (blue = benchmark)', fontsize=8.5)
B = P['breakeven_by_category']; cs = sorted(B, key=lambda c: -B[c]['n_serv'])[:12][::-1]
bp = pd.read_csv(f'{RES}/breakeven_products.csv.gz')
data = [bp[bp.branded_food_category == c].be_serv_median4.dropna().to_numpy() for c in cs]
bx = a2.boxplot(data, orientation='horizontal', widths=0.55, showfliers=False, patch_artist=True, medianprops={'color': INK})
for p_ in bx['boxes']: p_.set_facecolor('#d6e6f8'); p_.set_edgecolor(BLUE)
a2.set_yticks(np.arange(1, len(cs) + 1), [f"{short(c)} (n={len(d_)})" for c, d_ in zip(cs, data)], fontsize=7.5)
a2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'${v:.2f}'))
a2.set_xlabel('Breakeven price per labelled serving, US$'); a2.grid(axis='y', visible=False)
a2.set_title('Price per serving at which protein costs the same\nas the median of the four benchmarks', fontsize=8.5)
fig.tight_layout(); save(fig, 'fig3_prices', FIG)
print('ok')
