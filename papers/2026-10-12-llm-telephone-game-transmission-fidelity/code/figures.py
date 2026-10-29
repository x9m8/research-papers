"""Figures for the manuscript (300 dpi PNG + PDF). Run after restoration.py, fidelity.py, length_effect.py,
heterogeneity.py and compare.py. Palette as in paper 1; humans / chat models / base models are also
distinguished by marker shape and direct labels so identity never depends on colour alone."""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from data_load import CONDITIONS, TEMPERATURES
D = '../results/'; F = '../figures/'
HUM, CHAT, BASE = '#2a78d6', '#eb6834', '#1baf7a'
INK, MUTED, GRID = '#0b0b0b', '#52514e', '#e4e3df'
TEMP = ['#d6d1f5', '#ada3ec', '#8577e0', '#6250d6', '#3b2c9a']  # one hue, light -> dark = cool -> hot
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'lines.linewidth': 2, 'legend.frameon': False,
                     'axes.axisbelow': True})
R = json.load(open(D + 'restoration_results.json')); Fi = json.load(open(D + 'fidelity_results.json'))
LE = json.load(open(D + 'length_effect.json')); H = json.load(open(D + 'heterogeneity_results.json'))
C = json.load(open(D + 'compare_results.json'))
P1F = json.load(open('../paper1_results/fidelity_results.json'))
CHAT_L = [lab for _, lab in CONDITIONS[:5]]; BASE_L = [lab for _, lab in CONDITIONS[5:]]
short = {'GPT-3.5 Turbo': 'GPT-3.5', 'Llama 3 70B Instruct': 'Llama 70B', 'Llama 3 8B Instruct': 'Llama 8B',
         'Mixtral 8x7B Instruct': 'Mixtral', 'Mistral 7B Instruct': 'Mistral 7B', 'Llama 3 70B Base': 'Llama 70B base',
         'Mixtral 8x7B Base': 'Mixtral base', 'Gistr 1 (written)': 'Gistr 1', 'Gistr 2 (written)': 'Gistr 2',
         'Gistr 3 (written)': 'Gistr 3', 'Meylan et al. (spoken)': 'Meylan (spoken)'}
def save(fig, name):
    fig.savefig(F + name + '.png', dpi=300, bbox_inches='tight'); fig.savefig(F + name + '.pdf', bbox_inches='tight'); plt.close(fig)

# ---------- Figure 1: exact copies ----------
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1.05, 1]))
labs, vals, cols = [], [], []
for k in C['human']: labs.append(short[k]); vals.append(C['human'][k]['exact_rate']); cols.append(HUM)
for k in CHAT_L: labs.append(short[k]); vals.append(Fi['rephrase'][k]['exact_rate']); cols.append(CHAT)
for k in BASE_L: labs.append(short[k]); vals.append(Fi['rephrase'][k]['exact_rate']); cols.append(BASE)
y = np.arange(len(labs))[::-1]
ax[0].barh(y, vals, color=cols, height=0.62, edgecolor='white', linewidth=1)
for yi, v in zip(y, vals):
    ax[0].text(v + 0.012, yi, f'{v:.2f}' if v >= 0.005 else ('0' if v == 0 else f'{v:.4f}'), va='center', fontsize=7.5, color=INK)
ax[0].set_yticks(y); ax[0].set_yticklabels(labs); ax[0].set_xlim(0, 0.95); ax[0].grid(axis='y', visible=False)
ax[0].set_xlabel('Share of hand-offs that are exact copies')
for txt, yy, c in [('People', (y[1] + y[2]) / 2, HUM), ('Chat models', y[6], CHAT), ('Base models', (y[9] + y[10]) / 2, BASE)]:
    ax[0].text(0.94, yy, txt, ha='right', va='center', fontsize=8, color=INK, fontweight='bold')
ax[0].set_title('A  Exact copies', loc='left', fontsize=9, color=INK)
# Panel B: exact-copy rate vs length
for k, mk in [('Gistr exp 2', '-'), ('Meylan et al. (spoken)', '--')]:
    Ls = np.linspace(5, 66 if 'Gistr' in k else 20, 50); mu = P1F[k]['mu']
    ax[1].plot(Ls, np.exp(-mu * Ls), color=HUM, ls=mk, lw=2)
ax[1].text(80, 0.6, 'People, Gistr 2\n(fitted, paper 1)', color=INK, fontsize=7.5, ha='center')
ax[1].text(5.6, 0.33, 'People,\nspoken', color=INK, fontsize=7.5)
for k, mk in [('Llama 3 70B Base', 'o'), ('Mixtral 8x7B Base', 's')]:
    b = [x for x in LE[k]['binned'] if x['n'] >= 50]
    mids = [np.sqrt(max(x['lo'], 20) * min(x['hi'], 500)) for x in b]
    ax[1].plot(mids, [x['rate'] for x in b], color=BASE, marker=mk, ms=6, lw=1.5, markeredgecolor='white', markeredgewidth=1)
    ax[1].text(mids[-1] * 1.08, b[-1]['rate'], short[k], fontsize=7.5, color=INK, va='center')
ax[1].set_xscale('log'); ax[1].set_xlim(5, 1500); ax[1].set_ylim(0, 1)
ax[1].set_xlabel('Length of text passed on (words, log scale)'); ax[1].set_ylabel('Exact-copy probability')
ax[1].set_title('B  Copying and length run in opposite directions', loc='left', fontsize=9, color=INK)
fig.tight_layout(); save(fig, 'fig1_exact_copies')

# ---------- Figure 2: loss vs attraction ----------
fig, ax = plt.subplots(figsize=(5.2, 3.9))
ee = np.linspace(0.02, 0.26, 100)
for p in (0.05, 0.1, 0.2, 0.3, 0.4):
    ax.plot(ee, p * ee / (1 - p), color=GRID, lw=1.2, zorder=0)
    xe = 0.255 if p * 0.255 / (1 - p) < 0.058 else 0.058 * (1 - p) / p
    ax.text(xe, p * xe / (1 - p), f'{p:.2f}', fontsize=7, color=MUTED, ha='left', va='bottom')
ax.text(0.20, 0.0005, 'Grey lines: long-run share of\noriginal words, (a − a₀)/(e + a − a₀)', fontsize=7, color=MUTED)
for k, v in C['human'].items():
    ax.scatter(v['e'], v['a'] - v['a0'], color=HUM, marker='D', s=36, edgecolor='white', linewidth=1, zorder=3)
    ax.annotate(short[k], (v['e'], v['a'] - v['a0']), xytext=(4, -9 if 'Gistr 3' in k else 3), textcoords='offset points', fontsize=7, color=INK)
for k in CHAT_L + BASE_L:
    r = R['rephrase'][k]; c = CHAT if k in CHAT_L else BASE; m = 'o' if k in CHAT_L else 's'
    if k == 'Llama 3 8B Instruct': continue  # plotted as T = 0.8 in the temperature series
    ax.scatter(r['e'], r['attraction'], color=c, marker=m, s=40, edgecolor='white', linewidth=1, zorder=3)
    off = {'Mixtral 8x7B Instruct': (4, -10), 'Mistral 7B Instruct': (4, 2), 'GPT-3.5 Turbo': (-34, 3), 'Llama 3 70B Instruct': (-44, 3), 'Llama 3 70B Base': (-18, -13)}.get(k, (4, 2))
    ax.annotate(short[k], (r['e'], r['attraction']), xytext=off, textcoords='offset points', fontsize=7, color=INK)
Ts = [str(T) for T, _ in TEMPERATURES]
xs = [R['temperature'][t]['e'] for t in Ts]; ys = [R['temperature'][t]['attraction'] for t in Ts]
ax.plot(xs, ys, color=MUTED, lw=1, zorder=2)
for i, t in enumerate(Ts):
    ax.scatter(xs[i], ys[i], color=TEMP[i], marker='o', s=40, edgecolor=MUTED, linewidth=0.8, zorder=3)
    ax.annotate(f'T={t}', (xs[i], ys[i]), xytext=(-6, 6) if t == '0.0' else (0, -11), textcoords='offset points', fontsize=6.8, color=INK, ha='center')
ax.text(0.185, 0.0175, 'Llama 8B chat,\ntemperature sweep', fontsize=7, color=INK)
ax.set_xlim(0.02, 0.27); ax.set_ylim(0, 0.06)
ax.set_xlabel('Loss e (per word per hand-off)'); ax.set_ylabel('Reconstruction above chance, a − a₀')
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], marker='D', color=HUM, ls='', label='People (paper 1)'),
                   Line2D([], [], marker='o', color=CHAT, ls='', label='Chat models'),
                   Line2D([], [], marker='s', color=BASE, ls='', label='Base models'),
                   Line2D([], [], marker='o', color=TEMP[3], ls='', label='Llama 8B chat by temperature')], loc='center right', bbox_to_anchor=(1.0, 0.72), fontsize=7.5)
fig.tight_layout(); save(fig, 'fig2_loss_reconstruction')

# ---------- Figure 3: temperature ----------
fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.6), gridspec_kw=dict(width_ratios=[1, 1, 1.3]))
T = C['temperature']['T']
for j, (key, lab, ttl) in enumerate([('e', 'Loss e', 'A  Loss rises'), ('a', 'Reconstruction a', 'B  Reconstruction flat')]):
    v = [R['temperature'][str(t)][key] for t in T]; lo = [R['temperature'][str(t)][key + '_ci'][0] for t in T]
    hi = [R['temperature'][str(t)][key + '_ci'][1] for t in T]
    ax[j].errorbar(T, v, yerr=[np.array(v) - lo, np.array(hi) - v], color=TEMP[3], marker='o', ms=5, capsize=2, lw=1.8)
    ax[j].set_xlabel('Sampling temperature'); ax[j].set_ylabel(lab); ax[j].set_xticks(T)
    ax[j].set_ylim(0, 0.28 if key == 'e' else 0.03); ax[j].set_title(ttl, loc='left', fontsize=9, color=INK)
g = np.arange(51)
ylab = []
for i, t in enumerate(T):
    cur = R['temperature'][str(t)]['curve']
    ax[2].plot(g, cur, color=TEMP[i], lw=1.8); ylab.append(cur[-1])
for i in range(len(ylab) - 2, -1, -1):  # keep labels at least 0.065 apart
    ylab[i] = max(ylab[i], ylab[i + 1] + 0.065)
for i, t in enumerate(T):
    ax[2].text(51, ylab[i], f'T={t}', fontsize=7, color=INK, va='center')
ax[2].set_xlim(0, 58); ax[2].set_ylim(0, 1); ax[2].set_xlabel('Generation'); ax[2].set_ylabel('Seed words retained')
ax[2].set_title('C  Less of the original survives', loc='left', fontsize=9, color=INK)
fig.tight_layout(); save(fig, 'fig3_temperature')

# ---------- Figure 4: equilibrium ----------
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1.35, 1]))
for k in CHAT_L + BASE_L:
    h = H['rephrase'][k]; c = CHAT if k in CHAT_L else BASE
    ax[0].plot(g, R['rephrase'][k]['curve'], color=c, lw=1.5, alpha=0.9)
    ax[0].plot([41, 50], [h['plateau_pred']] * 2, color=c, lw=1, ls=':')
ax[0].text(20, 0.62, 'Chat models (orange) and base models (green):\nmean retention over 50 hand-offs.\nDotted: predicted long-run level.', fontsize=7, color=INK)
ax[0].set_xlim(0, 50); ax[0].set_ylim(0, 1); ax[0].set_xlabel('Generation'); ax[0].set_ylabel('Seed words retained')
ax[0].set_title('A  Chains approach a stable level', loc='left', fontsize=9, color=INK)
eq = C['equilibrium']
for n, p, o in zip(eq['names'], eq['pred'], eq['obs']):
    c = TEMP[3] if 'T=' in n else (CHAT if n in CHAT_L else BASE); m = 'o' if (n in CHAT_L or 'T=' in n) else 's'
    ax[1].scatter(p, o, color=c, marker=m, s=34, edgecolor='white', linewidth=1, zorder=3)
ax[1].plot([0, 0.4], [0, 0.4], color=MUTED, lw=1, ls='--'); ax[1].text(0.27, 0.245, 'y = x', fontsize=7, color=MUTED)
ax[1].set_xlim(0, 0.36); ax[1].set_ylim(0, 0.36)
ax[1].set_xlabel('Predicted (a − a₀)/(e + a − a₀)'); ax[1].set_ylabel('Observed, generations 41–50')
ax[1].text(0.02, 0.32, f"r = {eq['pearson_r']:.2f}, {eq['n']} conditions", fontsize=7.5, color=INK)
ax[1].set_title('B  Prediction vs observation', loc='left', fontsize=9, color=INK)
ax[1].legend(handles=[Line2D([], [], marker='o', color=CHAT, ls='', label='Chat models'), Line2D([], [], marker='s', color=BASE, ls='', label='Base models'),
                      Line2D([], [], marker='o', color=TEMP[3], ls='', label='Llama 8B, other temperatures')], loc='lower right', fontsize=7)
fig.tight_layout(); save(fig, 'fig4_equilibrium')
print('figures written')
