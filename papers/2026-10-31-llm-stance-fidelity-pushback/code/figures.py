"""Figures 1-3 from results/fidelity.json and results/extras.json."""
import json, numpy as np
from style import *
from common import RES, FIG, MODELS, SETTINGS, SET_LABEL, load_matrix, first_loss_chain
from fidelity import km_curve

F = json.load(open(f'{RES}/fidelity.json')); X = json.load(open(f'{RES}/extras.json'))
names = {k: v[0] for k, v in MODELS.items()}
order = sorted(MODELS, key=lambda k: F['main']['factual'][k]['r'])  # order models by factual retention

# Figure 1: survival curves, observed (lines) vs constant-retention prediction (dashed), three panels
fig, axs = plt.subplots(1, 3, figsize=(10, 3.6), sharey=True)
t = np.arange(1, 6)
for ax, s in zip(axs, SETTINGS):
    for k in MODELS:
        S = km_curve(load_matrix(s, MODELS[k][1][s]))
        m = F['main'][s][k]; pred = m['p1'] * m['r'] ** (t - 1)
        ax.plot(t, S, color=SETCOL[s], lw=1.2, alpha=0.55, marker=SETMARK[s], ms=3)
        ax.plot(t, pred, color=MUTED, lw=0.7, ls=':', alpha=0.8)
    mm = F['main'][s]['_mean_over_models']
    ax.set_title(f"{SET_LABEL[s]}  ·  mean r = {mm['r']:.2f}", fontsize=9, color=INK, loc='left')
    ax.set_xticks(t); ax.set_xticklabels(['1\n(first\nanswer)', '2', '3', '4', '5'])
    ax.set_xlabel('Turn (pushbacks after turn 1)')
    ax.set_ylim(0, 1.02)
axs[0].set_ylabel('Share of items holding the stance\nat every turn so far')
from matplotlib.lines import Line2D
fig.legend([Line2D([], [], color=MUTED, lw=1.2), Line2D([], [], color=MUTED, ls=':', lw=0.8)],
           ['Observed (one line per model)', 'Constant per-turn retention, p₁·rᵗ⁻¹'], loc='lower center', ncol=2, fontsize=8, bbox_to_anchor=(0.5, -0.04))
fig.tight_layout(rect=(0, 0.05, 1, 1)); save(fig, 'fig1_survival', FIG)

# Figure 2: per-turn retention r by model and setting with 95% cluster-bootstrap intervals
fig, ax = plt.subplots(figsize=(6.6, 4.6))
y = np.arange(len(order))
off = {'factual': -0.22, 'stereotype': 0, 'debate': 0.22}
for s in SETTINGS:
    r = [F['main'][s][k]['r'] for k in order]; ci = np.array([F['boot'][s][k]['r'] for k in order])
    ax.errorbar(r, y + off[s], xerr=[np.array(r) - ci[:, 0], ci[:, 1] - np.array(r)], fmt=SETMARK[s], color=SETCOL[s], ms=5,
                elinewidth=1, capsize=0, label=SET_LABEL[s], mec='white', mew=0.6)
ax.set_yticks(y); ax.set_yticklabels([names[k] for k in order])
ax.set_xlabel('Per-turn retention r = P(keeps stance at next pushback | held so far)')
ax.set_xlim(0.2, 1.01); ax.legend(loc='lower left', fontsize=7.5)
fig.tight_layout(); save(fig, 'fig2_retention', FIG)

# Figure 3: (A) pooled turn-specific retention by setting; (B) debate change probabilities by current position
fig, axs = plt.subplots(1, 2, figsize=(9.2, 3.6), gridspec_kw={'width_ratios': [1, 1.25]})
ax = axs[0]
for s in SETTINGS:
    c = F['constancy'][s]
    ax.plot([2, 3, 4, 5], c['pooled_r_t'], marker=SETMARK[s], color=SETCOL[s], lw=2, ms=6, label=SET_LABEL[s], mec='white', mew=0.6)
ax.set_xticks([2, 3, 4, 5]); ax.set_xlabel('Turn'); ax.set_ylabel('Retention at this turn, all 11 models pooled')
ax.set_ylim(0.7, 1.0); ax.legend(fontsize=7, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=1); ax.set_title('A  Retention is not constant across turns', loc='left', fontsize=9)
ax = axs[1]
dc = X['debate_change']
ks = [k for k in sorted(MODELS, key=lambda k: dc[k]['p_change_from_stance']) if dc[k]['n_from_other'] >= 10]
yy = np.arange(len(ks))
ax.scatter([dc[k]['p_change_from_stance'] for k in ks], yy, color=GREEN, marker='^', s=36, label='From the assigned stance (gives it up)', zorder=3, edgecolor='white', lw=0.6)
ax.scatter([dc[k]['p_change_from_other'] for k in ks], yy, color=INK, marker='o', s=30, facecolor='white', label='From a conceded position (switches back)', zorder=3)
for i, k in enumerate(ks): ax.plot([dc[k]['p_change_from_stance'], dc[k]['p_change_from_other']], [i, i], color=LIGHT, lw=1, zorder=1)
ax.set_yticks(yy); ax.set_yticklabels([names[k] for k in ks]); ax.set_xlim(-0.02, 1.02)
ax.set_xlabel('P(position changes after "I do not agree")')
ax.legend(fontsize=7, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2); ax.set_title('B  Debate: change after a direction-free challenge', loc='left', fontsize=9)
fig.tight_layout(); save(fig, 'fig3_turns_debate', FIG)
print('ok', ks)
