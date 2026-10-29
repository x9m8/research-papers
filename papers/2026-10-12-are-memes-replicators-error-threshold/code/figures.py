"""Synthesis table and figures for the manuscript. Run after fidelity.py, restoration.py, heterogeneity.py, theory.py."""
import json, numpy as np, matplotlib, matplotlib.ticker
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from theory import equilibrium
D = '../results/'; F = '../figures/'
C = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6']
INK, MUTED, GRID = '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'lines.linewidth': 2, 'legend.frameon': False})
fid = json.load(open(D + 'fidelity_results.json')); cur = json.load(open(D + 'fidelity_curves.json'))
res = json.load(open(D + 'restoration_results.json')); het = json.load(open(D + 'heterogeneity_results.json'))
th = json.load(open(D + 'theory_results.json'))

# ---------- Table 1 ----------
rows = []
names = {'Gistr exp 1': 'Written recall, everyday sentences (Gistr 1)', 'Gistr exp 2': 'Written recall, film-quote sentences (Gistr 2)',
         'Gistr exp 3': 'Written recall, news items and story openings (Gistr 3)', 'Meylan et al. (spoken)': 'Spoken sentences heard in noise (Meylan et al.)',
         'Cornish et al. (letter strings)': 'Recall of letter-string sets (Cornish et al.)'}
for k, v in fid.items():
    mu = v['mu']; L = v['mean_L']
    rows.append(dict(dataset=names[k], unit='letter' if 'Cornish' in k else 'word', n=v['n_transmissions'], items=v['n_items'], mean_L=L,
                     Q_obs=v['Q_obs'], mu=mu, mu_ci=v['mu_ci'], s_req_meanL=float(np.exp(mu * L) - 1),
                     Lstar_s02=float(np.log(1.2) / mu), Lstar_s1=float(np.log(2) / mu), Lstar_s9=float(np.log(10) / mu)))
json.dump(rows, open(D + 'table1.json', 'w'), indent=1)
for r in rows: print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in r.items()})

# ---------- Figure 1: theory ----------
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9))
Ls = np.arange(1, 41)
for i, (a, lab) in enumerate([(0.0, 'a = 0'), (0.02, 'a = 0.02'), (0.1, 'a = 0.10')]):
    ax[0].plot(Ls, th['intact_vs_L'][f'e=0.12,a={a},s=1.0'], color=C[i], label=lab)
Lst = np.log(2) / -np.log(1 - 0.12)
ax[0].axvline(Lst, color=MUTED, lw=1, ls='--'); ax[0].text(Lst + 0.4, 0.55, 'L* (a = 0)', color=MUTED, fontsize=8)
ax[0].set_xlim(1, 20); ax[0].set_xlabel('Item length L (units)'); ax[0].set_ylabel('Equilibrium frequency of intact item')
ax[0].set_title('A  Error threshold (e = 0.12, s = 1)', loc='left', fontsize=9, color=INK); ax[0].legend(fontsize=8)
sims = []
for a in (0.0, 0.02, 0.1):
    ys = []
    for L in Ls:
        v = equilibrium(int(L), 0.12, a, 1.0); ys.append(sum(v[k] * (L - k) / L for k in range(L + 1)))
    sims.append(ys)
for i, a in enumerate((0.0, 0.02, 0.1)):
    ax[1].plot(Ls, sims[i], color=C[i], label=('a = 0' if a == 0 else f'a = {a}'))
    if a > 0: ax[1].axhline(a / (a + 0.12), color=C[i], lw=1, ls=':')
ax[1].set_xlim(1, 40); ax[1].set_ylim(0, 1); ax[1].set_xlabel('Item length L (units)'); ax[1].set_ylabel('Mean share of canonical units')
ax[1].set_title('B  Gist persists by reconstruction', loc='left', fontsize=9, color=INK)
ax[1].text(40, 0.1 / 0.22 + 0.03, 'a/(a+e)', color=MUTED, fontsize=7, ha='right'); ax[1].text(40, 0.02 / 0.14 + 0.03, 'a/(a+e)', color=MUTED, fontsize=7, ha='right'); ax[1].legend(fontsize=8, loc='upper right')
fig.tight_layout(); fig.savefig(F + 'fig1_theory.png', dpi=300); fig.savefig(F + 'fig1_theory.pdf')

# ---------- Figure 2: exact-copy probability vs length ----------
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={'width_ratios': [1.35, 1]}); ax = axs[0]
mk = ['o', 's', '^', 'D', 'v']
for i, (k, cv) in enumerate(cur.items()):
    cv = np.array(cv); mu = fid[k]['mu']
    ax.plot(cv[:, 0], cv[:, 1], mk[i], color=C[i], ms=6, mec='white', mew=1, label=names[k].split(' (')[0] if False else k.replace(' (spoken)', '').replace(' (letter strings)', ''))
    xx = np.linspace(1, cv[:, 0].max() * 1.05, 100); ax.plot(xx, np.exp(-mu * xx), color=C[i], lw=1.5, ls=(0, (4, 2)) if 'exp 1' in k else '-')
ax.set_xlabel('Length of the text copied (units: words; letters for Cornish)'); ax.set_ylabel('Probability of an exact copy, Q')
ax.set_ylim(0, 1); ax.legend(fontsize=7, loc='upper right'); ax.set_title('A  Exact-copy probability and length', loc='left', fontsize=9, color=INK)
dep = json.load(open(D + 'fidelity_by_depth.json'))
for i, k in enumerate(['Gistr exp 1', 'Gistr exp 2', 'Gistr exp 3', 'Meylan et al. (spoken)']):
    d = dep[k]; xs = np.arange(len(d)) + (i - 1.5) * 0.12
    mu = [x['mu'] for x in d]; lo = [x['mu'] - x['mu_ci'][0] for x in d]; hi = [x['mu_ci'][1] - x['mu'] for x in d]
    axs[1].errorbar(xs, mu, yerr=[lo, hi], fmt=mk[i] + '-', color=C[i], ms=5, mec='white', lw=1.5, capsize=2, label=k.replace(' (spoken)', ''))
axs[1].set_xticks(range(4)); axs[1].set_xticklabels(['1', '2–3', '4–6', '7+']); axs[1].set_xlabel('Generation'); axs[1].set_ylabel('Per-word error rate μ')
axs[1].set_ylim(0, 0.16); axs[1].set_title('B  Error rate by generation', loc='left', fontsize=9, color=INK); axs[1].legend(fontsize=7, loc='upper right', ncol=2)
fig.tight_layout()
fig.savefig(F + 'fig2_fidelity.png', dpi=300); fig.savefig(F + 'fig2_fidelity.pdf')

# ---------- Figure 3: loss vs restoration ----------
fig, ax = plt.subplots(figsize=(5.4, 3.0))
keys = list(res); x = np.arange(len(keys)); w = 0.26
for j, (fld, lab) in enumerate([('e', 'loss rate e'), ('a', 'reconstruction rate a'), ('a0', 'chance entry a₀')]):
    vals = [res[k][fld] for k in keys]; ci = np.array([res[k][fld + '_ci'] for k in keys])
    ax.bar(x + (j - 1) * w, vals, w * 0.92, color=C[j], label=lab)
    ax.errorbar(x + (j - 1) * w, vals, yerr=[np.array(vals) - np.maximum(ci[:, 0], 6e-5), ci[:, 1] - np.array(vals)], fmt='none', ecolor=INK, lw=0.8, capsize=2)
ax.set_yscale('log'); ax.set_ylim(5e-5, 0.3); ax.set_xticks(x); ax.set_xticklabels([k.replace(' (content words)', '').replace(' (all words)', '') for k in keys], fontsize=8)
ax.set_ylabel('Per-word, per-generation probability'); ax.legend(fontsize=7, ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.13)); fig.tight_layout()
fig.savefig(F + 'fig3_restoration.png', dpi=300); fig.savefig(F + 'fig3_restoration.pdf')

# ---------- Figure 4: retention curves observed vs models ----------
sets = ['Gistr exp 2', 'Gistr exp 3', 'Meylan et al.']
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
for i, k in enumerate(sets):
    h = het[k]; t = np.arange(h['G'] + 1)
    ax[i].plot(t, h['observed'], 'o', color=INK, ms=4, label='observed (held-out chains)')
    ax[i].plot(t, h['heterogeneous'], color=C[0], label='word-specific e, a')
    ax[i].plot(t, h['heterogeneous_no_restoration'], color=C[1], ls='--', label='word-specific e, a = 0')
    ax[i].plot(t, h['homogeneous'], color=C[2], ls=':', label='pooled e, a')
    ax[i].set_title(k, loc='left', fontsize=9, color=INK); ax[i].set_xlabel('Generation'); ax[i].set_ylim(0, 1.02); ax[i].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
ax[0].set_ylabel('Share of seed words present'); h, l = ax[2].get_legend_handles_labels(); fig.legend(h, l, fontsize=7, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.01)); fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(F + 'fig4_curves.png', dpi=300); fig.savefig(F + 'fig4_curves.pdf')

# ---------- Figure 5: replicator length vs selection ----------
fig, ax = plt.subplots(figsize=(4.8, 3.3))
s = np.logspace(-2, 1.3, 200)
for i, k in enumerate(['Gistr exp 2', 'Gistr exp 3', 'Meylan et al. (spoken)']):
    mu = fid[k]['mu']; ax.plot(s, np.log(1 + s) / mu, color=C[i], label=k.replace(' (spoken)', '') + f'  (μ = {mu:.3f}/word)')
ax.axvline(0.2, color=MUTED, lw=1, ls='--'); ax.text(0.21, 100, 's = 0.2', ha='left', va='top', fontsize=7, color=MUTED)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_ylim(0.5, 120)
ax.set_xlabel('Selective advantage of the intact item, s'); ax.set_ylabel('Longest maintainable item, L* (words)')
ax.legend(fontsize=7, loc='lower right'); fig.tight_layout()
fig.savefig(F + 'fig5_replicator_length.png', dpi=300); fig.savefig(F + 'fig5_replicator_length.pdf')
print('figures written')
