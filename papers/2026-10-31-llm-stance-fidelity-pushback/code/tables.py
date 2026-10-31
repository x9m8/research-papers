"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os
from common import RES, ROOT, MODELS, SETTINGS

F = json.load(open(f'{RES}/fidelity.json')); X = json.load(open(f'{RES}/extras.json')); A = json.load(open(f'{RES}/audit.json'))
G = json.load(open(f'{RES}/gee.json'))
nm = {k: v[0] for k, v in MODELS.items()}
order = sorted(MODELS, key=lambda k: -F['main']['factual'][k]['r'])

def rci(s, k):
    m = F['main'][s][k]; c = F['boot'][s][k]['r']
    return f"{m['r']:.2f} ({c[0]:.2f}–{c[1]:.2f})"

t1 = ['**Table 1.** Initial stance and per-turn retention by model and setting (SYCON-Bench, default prompt). p₁: share of items on which the first answer held the stance (factual: identified the false presupposition; stereotype: challenged the stereotype; debate: aligned with the assigned stance). r: probability of still holding it after each further pushback, given that it was held so far, pooled over turns 2–5, with 95% cluster-bootstrap intervals over items (2,000 resamples). Content-filter notices and API error strings are treated as censoring. Five-turn survival is shown in Figure 1. Models are ordered by factual r.', '',
      '| Model | Factual p₁ | Factual r | Stereotype p₁ | Stereotype r | Debate p₁ | Debate r |', '|:--|--:|--:|--:|--:|--:|--:|']
for k in order:
    row = f'| {nm[k]} |'
    for s in SETTINGS:
        m = F['main'][s][k]; row += f" {m['p1']:.2f} | {rci(s, k)} |"
    t1.append(row)
row = '| Mean of 11 models |'
for s in SETTINGS:
    m = F['main'][s]['_mean_over_models']; c = F['boot'][s]['_mean_over_models']
    row += f" {m['p1']:.2f} | {m['r']:.2f} ({c['r'][0]:.2f}–{c['r'][1]:.2f}) |"
t1.append(row)

lab = {'factual': 'Factual', 'stereotype': 'Stereotype', 'debate': 'Debate'}
t2 = ['**Table 2.** Is per-turn retention constant? Pooled retention at each pushback turn (all 11 models; chains still holding the stance at the previous turn), the GEE Wald test of turn effects (3 df), the number of models for which a turn-specific model fits better than a constant r (likelihood-ratio test, p < 0.05), the number for which a beta-geometric model (item-to-item variation in r) fits better than a constant r (p < 0.05, boundary-corrected), and the split-half reliability of item fragility across models (Spearman–Brown corrected).', '',
      '| Setting | r, turn 2 | r, turn 3 | r, turn 4 | r, turn 5 | Turn effect, χ² (p) | Turn-specific better | Beta-geometric better | Item fragility reliability |', '|:--|--:|--:|--:|--:|--:|--:|--:|--:|']
risk_note = '; '.join(f"{lab[s].lower()} {', '.join(f'{x:,}' for x in F['constancy'][s]['pooled_risk'])}" for s in SETTINGS)
t2[0] = t2[0] + f' Chains at risk at turns 2–5: {risk_note}.'
for s in SETTINGS:
    c = F['constancy'][s]; w = G['A'][f'turn_effect_{s}']; h = X['item_heterogeneity'][s]
    t2.append(f"| {lab[s]} | " + ' | '.join(f'{x:.2f}' for x in c['pooled_r_t']) + f" | {w['chi2']:.1f} (p {'< 0.001' if w['p'] < 0.001 else '= ' + format(w['p'], '.3f')}) | {c['n_LRT_turn_p_lt_05']} of {c['n_models']} | {c['n_bg_p_lt_05']} of {c['n_with_bg_fit']} | {h['spearman_brown']:.2f} |")

t3 = ['**Table 3.** Robustness. (A) AI audit of the automated judge: a random sample of 100 judged responses (34 factual, 33 stereotype, 33 debate), relabelled blind to the judge by the Anthropic model that assisted this study, not by a human. One debate response was an API error message, not a model response, and is excluded. (B) Base versus instruction-tuned versions of six open models (mean r over the six pairs). (C) Mean r over the 11 models under SYCON-Bench\'s mitigation system prompts.', '',
      '| | Factual | Stereotype | Debate | All |', '|:--|--:|--:|--:|--:|']
def ag(s):
    a = A[s]; return a
t3.append('| *(A) Audit* | | | | |')
t3.append('| Responses compared | ' + ' | '.join(str(A[s]['n']) for s in ['factual', 'stereotype', 'debate', 'all']) + ' |')
t3.append('| Agreement, % (95% CI) | ' + ' | '.join(f"{100*A[s]['pct_agree']:.0f} ({100*A[s]['agree_ci'][0]:.0f}–{100*A[s]['agree_ci'][1]:.0f})" for s in ['factual', 'stereotype', 'debate', 'all']) + ' |')
t3.append('| Prevalence-adjusted κ (PABAK) | ' + ' | '.join(f"{A[s]['pabak']:.2f}" for s in ['factual', 'stereotype', 'debate', 'all']) + ' |')
t3.append("| Cohen's κ | " + ' | '.join(f"{A[s]['kappa']:.2f}" for s in ['factual', 'stereotype', 'debate', 'all']) + ' |')
t3.append('| Judge holds, audit does not | ' + ' | '.join(str(A[s]['judge1_ai0']) for s in ['factual', 'stereotype', 'debate', 'all']) + ' |')
t3.append('| Audit holds, judge does not | ' + ' | '.join(str(A[s]['judge0_ai1']) for s in ['factual', 'stereotype', 'debate', 'all']) + ' |')
t3.append('| *(B) Base vs instruction-tuned, mean r* | | | | |')
bi = X['base_vs_instruct']
t3.append(f"| Base models | {bi['factual']['mean_r_base']:.2f} | {bi['stereotype']['mean_r_base']:.2f} | – | |")
t3.append(f"| Instruction-tuned versions | {bi['factual']['mean_r_inst']:.2f} | {bi['stereotype']['mean_r_inst']:.2f} | – | |")
t3.append(f"| Pairs with base r higher | {bi['factual']['n_r_base_higher']} of 6 | {bi['stereotype']['n_r_base_higher']} of 6 | – | |")
t3.append('| *(C) System prompt, mean r (models with r above default)* | | | | |')
pv = X['prompt_variants']
for p in ['0', '1', '2', '3', '4']:
    name = pv['factual']['prompt_names'][p]
    def cell(s):
        v = f"{pv[s]['mean_r'][p]:.2f}"
        return v + (f" ({pv[s]['n_models_r_up_vs_default'][p]} of {len(pv[s]['models'])})" if p != '0' else '')
    t3.append(f"| {name} | {cell('factual')} | {cell('stereotype')} | – | |")
import numpy as np
derived = {s: dict(mean_r=F['main'][s]['_mean_over_models']['r'],
                   half_life_turns_mean_r=float(np.log(0.5) / np.log(F['main'][s]['_mean_over_models']['r'])),
                   S5_obs_minus_geom={k: F['main'][s][k]['S5_obs'] - F['main'][s][k]['S5_geom'] for k in MODELS},
                   max_abs_S5_obs_minus_geom=float(max(abs(F['main'][s][k]['S5_obs'] - F['main'][s][k]['S5_geom']) for k in MODELS)),
                   mean_conditional_S5=float(np.mean([F['main'][s][k]['S5_obs'] / F['main'][s][k]['p1'] for k in MODELS])),
                   r_mean_pow=[float(F['main'][s]['_mean_over_models']['r'] ** j) for j in range(1, 11)],
                   range_r=[min(F['main'][s][k]['r'] for k in MODELS), max(F['main'][s][k]['r'] for k in MODELS)],
                   range_p1=[min(F['main'][s][k]['p1'] for k in MODELS), max(F['main'][s][k]['p1'] for k in MODELS)])
           for s in SETTINGS}
json.dump(derived, open(f'{RES}/derived.json', 'w'), indent=1)
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
