"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os
from common import RES, ROOT, SCEN
P = json.load(open(f'{RES}/prevalence.json'))
def f(v): return f"{100*v[0]:.1f}" + (f" ({100*v[1]:.1f})" if v[1] else '')
rows = [('PROT_ear_refwt', 'Protein < EAR (0.66 g/kg reference weight)'), ('ZINC', 'Zinc'), ('FDFE', 'Folate (DFE)'), ('CALC', 'Calcium'), ('MAGN', 'Magnesium'),
        ('VARA', 'Vitamin A (RAE)'), ('VC', 'Vitamin C'), ('VD', 'Vitamin D'), ('ATOC', 'Vitamin E'), ('VB12', 'Vitamin B12'), ('IRON', 'Iron (men; women 51+)')]
sc = list(SCEN)
M = P['L']['meta']
t1 = [f"**Table 1.** Estimated share of US adults eligible for GLP-1 obesity treatment whose usual intake from food would fall below the EAR, at their current diet and after proportional cuts in everything eaten. NHANES August 2021–August 2023, adults 20 and over with BMI ≥30, or ≥27 with diabetes or hypertension, not pregnant, two reliable 24-hour recalls (n = {M['n_two_day']:,}). Survey-weighted percentages (standard errors).", '',
      '| Nutrient | ' + ' | '.join(s.replace('Baseline', 'Usual diet') for s in sc) + ' |', '|:--|' + '--:|' * len(sc)]
for k, l in rows: t1.append(f'| {l} | ' + ' | '.join(f(P['L']['res'][s][k]) for s in sc) + ' |')
t1.append('| *Below other protein yardsticks* |' + ' |' * len(sc))
for k, l in [('PROT_ear_adjwt', 'Protein < 0.66 g/kg adjusted weight'), ('PROT_ear_actualwt', 'Protein < 0.66 g/kg actual weight'), ('PROT_below_1.2_refwt', 'Protein < 1.2 g/kg reference weight'), ('PROT_below_80g', 'Protein < 80 g/day')]:
    t1.append(f'| {l} | ' + ' | '.join(f(P['L']['res'][s][k]) for s in sc) + ' |')
t1.append('| *At or above the Adequate Intake* |' + ' |' * len(sc))
for k, l in [('POTA_above_AI', 'Potassium'), ('FIBE_above_AI', 'Fibre'), ('CHL_above_AI', 'Choline'), ('VK_above_AI', 'Vitamin K')]:
    t1.append(f'| {l} | ' + ' | '.join(f(P['L']['res'][s][k]) for s in sc) + ' |')
t1.append('| Mean energy, kcal/day | ' + ' | '.join(f"{P['L']['res'][s]['mean_kcal'][0]:,.0f}" for s in sc) + ' |')
t1.append('| Mean protein, g/day | ' + ' | '.join(f"{P['L']['res'][s]['mean_prot'][0]:.1f}" for s in sc) + ' |')
t2 = ['**Table 2.** Sensitivity: share below the EAR on the usual diet and at a 35% proportional cut in food, by survey cycle and with dietary supplements. NHANES 2017–March 2020 includes 24-hour supplement recalls; supplement intake was added after estimating usual food intake and was not reduced. Percentages (standard errors).', '',
      '| Nutrient | Usual diet: 2021–2023, food | Usual diet: 2017–2020, food | Usual diet: 2017–2020, food + supplements | −35%: 2021–2023, food | −35%: 2017–2020, food | −35%: 2017–2020, food + supplements |', '|:--|--:|--:|--:|--:|--:|--:|']
s35 = 'Semaglutide 2.4 mg, −35%'
for k, l in rows: t2.append(f"| {l} | {f(P['L']['res']['Baseline'][k])} | {f(P['P']['res']['Baseline'][k])} | {f(P['P_supp']['res']['Baseline'][k])} | {f(P['L']['res'][s35][k])} | {f(P['P']['res'][s35][k])} | {f(P['P_supp']['res'][s35][k])} |")
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables[:3000])
