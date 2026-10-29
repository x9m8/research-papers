"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md."""
import os, json
import pandas as pd
from common import RES, ROOT, CODES, CODE_LABEL

P = pd.read_csv(f'{RES}/prevalence.csv').set_index('code')
A = pd.read_csv(f'{RES}/agreement.csv').set_index('variable')
B = pd.read_csv(f'{RES}/prevalence_by_seller.csv')
ORDER = ['Telehealth platform', 'Clinic / med spa', 'Online pharmacy / marketplace', 'Research-chemical seller',
         'Compounder (503A/503B)', 'API supplier / other manufacturer']
SHORT = ['Telehealth', 'Clinic/med spa', 'Online pharmacy', 'Research chemical', 'Compounder', 'API/other']
N = int(P.N.iloc[0])
def k(v): return '–' if pd.isna(v) else f'{v:.2f}'

t1 = [f'**Table 1.** Violations, claims and letter features cited by FDA in {N} included warning letters (issued 2 October 2023 to 24 September 2026), with Wilson 95% confidence intervals, and agreement between the rule-based coder and the reader before adjudication (all 163 retrieved letters). κ is undefined when both coders are constant.', '',
      '| Code | Letters, n | % (95% CI) | Agreement, % | κ |', '|:--|--:|--:|--:|--:|']
sections = [('*Statutory violations alleged*', [c for c in CODES if c.startswith('V_')]), ('*Claims and marketing features cited*', [c for c in CODES if c.startswith('C_')]),
            ('*Letter features*', [c for c in CODES if c.startswith('F_')])]
for title, cs in sections:
    t1.append(f'| {title} | | | | |')
    for c in cs:
        r = P.loc[c]; a = A.loc[c]
        t1.append(f"| {CODE_LABEL[c]} | {int(r.n)} | {100*r.pct:.1f} ({100*r.lo:.1f}–{100*r.hi:.1f}) | {100*a.pct_agree:.1f} | {k(a.kappa)} |")
for v, lab in [('eligible', 'Eligibility (include/exclude)'), ('seller_type', 'Seller type (8 categories)')]:
    a = A.loc[v]; t1.append(f'| {lab} | | | {100*a.pct_agree:.1f} | {k(a.kappa)} |')

Nn = B.groupby('group').N.first()
t2 = [f'**Table 2.** Selected violations and claims by seller type: number of letters (% of letters to that seller type). Seller type as coded from the letter text; compounders combine 503A pharmacies (n = 3) and 503B outsourcing facilities (n = 6).', '',
      '| Code | ' + ' | '.join(f'{s} (n = {Nn[g]})' for s, g in zip(SHORT, ORDER)) + ' |', '|:--|' + '--:|' * len(ORDER)]
sel = ['V_unapproved', 'V_misbrand_502f1', 'V_rx_503b1', 'V_misbrand_502bb', 'V_cgmp', 'V_sterility', 'V_503A_conditions', 'V_503B_conditions', 'V_other_peptide',
       'C_sameness', 'C_generic', 'C_fda_approved', 'C_firm_branded', 'C_brand_names', 'C_research_disguise', 'C_no_rx']
Bi = B.set_index(['code', 'group'])
for c in sel:
    t2.append(f'| {CODE_LABEL[c]} | ' + ' | '.join(f"{int(Bi.loc[(c, g)].n)} ({100*Bi.loc[(c, g)].pct:.0f})" for g in ORDER) + ' |')
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
