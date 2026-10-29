"""Tables 1-2 -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os, pandas as pd
from common import DATA, RES, ROOT
e = pd.read_csv(f'{RES}/effects_all.csv'); x = pd.read_csv(f'{DATA}/extraction.csv')
short = {'Corrigan2012': 'Corrigan (2012)', 'Hardie2015': 'Hardie et al. (2015)', 'Hyun2018': 'Hyun & Ryew (2018)', 'Hyung2016': 'Hyung et al. (2016)',
         'Negrini2007': 'Negrini & Negrini (2007)', 'Ozgul2012': 'Ozgul et al. (2012)', 'Rodrigues2020': 'Rodrigues et al. (2020)', 'Shin2016': 'Shin & Yoo (2016)',
         'Sussman2001': 'Sussman et al. (2001)', 'Tajik2026': 'Tajik et al. (2026)', 'Tseng2011': 'Tseng & Liu (2011)', 'Yoon2014': 'Yoon (2014)', 'Suzuki2025': 'Suzuki et al. (2025)'}
desc = {
 'Hardie2015': ('UK', '12 F, 21 y', 'One-shoulder and cross-body bag, 10% BM', 'Treadmill, 5 min', 'Trunk and shoulder EMG'),
 'Yoon2014': ('South Korea', '20, 23 y', 'One-shoulder bag, 10% BM, three strap lengths', 'Treadmill, 5 min', 'Trapezius and erector spinae EMG'),
 'Hyung2016': ('South Korea', '16, 21 y', 'Hand, one-shoulder and cross-body bag, 5/10/15% BM', 'Overground', 'Pelvic tilt and rotation'),
 'Corrigan2012': ('Canada', '15 M, 23 y', 'Shoulder-carried hockey bag, 10/20/30% BM', 'Overground', 'Gait; erector spinae EMG'),
 'Rodrigues2020': ('Brazil', '258 F (143 and 61 analysed by side), 18–59 y', "Participant's own shoulder bag (right or left), mostly ≤5% BM", 'Overground, 2 m plate', 'Gait'),
 'Sussman2001': ('USA', '10, students', 'One-strap bag on one shoulder, 5.9 kg', 'Treadmill', 'Trunk and head angles'),
 'Shin2016': ('South Korea', '10 F, 81 y', 'Hand-held bag, ~0.2 kg', 'Turning gait', 'Gait speed; trunk acceleration'),
 'Tseng2011': ('Taiwan', '9 M, 22 y', 'Hand-held bag of books, 10% BM', 'Stairs', 'Heart rate; perceived exertion; trunk flexion'),
 'Hyun2018': ('South Korea', '9 M, 23 y', '20 kg barbell at one side (not a bag)', 'Overground', 'Gait; balance; ground force'),
 'Tajik2026': ('Iran', '30 M (15 with chronic low back pain), 23–28 y', 'Dumbbell in one hand, 10/20% BM (not a bag)', 'Overground', 'Lumbar EMG (means only)'),
 'Suzuki2025': ('Japan', '26 young adults', 'One-shoulder and cross-body bag', 'Walking 10 min, in-shoe sensors', 'Gait (figures only)'),
 'Negrini2007': ('Italy', '43, 12–13 y (adolescents)', 'One-strap 8 kg load', 'Standing', 'Spinal posture'),
 'Ozgul2012': ('Turkey', '20 M, 13 y (adolescents)', 'Backpack on one shoulder, 15% BM', 'Overground', 'Pelvic kinematics')}
t1 = ['**Table 1.** Studies included after full-text reading (n = 13). BM, body mass; EMG, electromyography; F, female; M, male. Ages are means.', '',
      '| Study | Country | Participants | Load carried | Task | Outcomes |', '|:--|:--|:--|:--|:--|:--|']
for k, v in desc.items(): t1.append(f'| {short[k]} | ' + ' | '.join(v) + ' |')
def g(sid, cond):
    r = e[(e.study_id == sid) & e.vs_noload & cond(e)]
    return r
rows = []
def add(label, r, note=''):
    for q in r.itertuples():
        rows.append(f"| {label} | {short[q.study_id]} | {q.carry_mean:g} vs {q.comparison_mean:g} | {q.g:.2f} ({q._asdict()['_31'] if False else ''}{q._asdict().get('lo_0.5', '')}) |")
t2 = ['**Table 2.** The most consistent findings, adult studies versus carrying nothing. g: within-study standardised difference (Hedges); 95% CI assumes a between-condition correlation of 0.5. EMG in %MVC (Hardie) or as reported (Yoon; unit labelling ambiguous). Strap or bag side as reported by the authors.', '',
      '| Finding | Study | Carrying vs not carrying | g (95% CI) |', '|:--|:--|:--|:--|']
def row(lbl, q): t2.append(f"| {lbl} | {short[q.study_id]} | {q.carry_mean:g} vs {q.comparison_mean:g} | {q.g:.2f} ({q._30:.2f} to {q._31:.2f}) |")
E = e.rename(columns={'lo_0.5': 'lo', 'hi_0.5': 'hi'})
def row(lbl, q): t2.append(f"| {lbl} | {short[q.study_id]} | {q.carry_mean:g} vs {q.comparison_mean:g} | {q.g:.2f} ({q.lo:.2f} to {q.hi:.2f}) |")
sel = E[E.vs_noload]
for q in sel[(sel.study_id == 'Hardie2015') & sel.outcome_name.str.startswith('Trapezius left')].itertuples():
    row('Strap-side upper trapezius, ' + ('one-shoulder bag' if 'one-shoulder' in q.bag_type else 'cross-body bag'), q)
for q in sel[(sel.study_id == 'Yoon2014') & sel.outcome_name.str.startswith('Upper trapezius right')].itertuples():
    row('Bag-side upper trapezius, one-shoulder bag, strap ' + q.outcome_name.split('bag at ')[1], q)
for q in sel[(sel.study_id == 'Hardie2015') & sel.outcome_name.str.startswith('Erector spinae right') & sel.bag_type.str.contains('one-shoulder')].itertuples():
    row('Opposite-side erector spinae, one-shoulder bag', q)
for q in sel[(sel.study_id == 'Yoon2014') & sel.outcome_name.str.startswith('Erector spinae left')].itertuples():
    row('Opposite-side erector spinae, strap ' + q.outcome_name.split('bag at ')[1], q)
for q in sel[(sel.study_id == 'Corrigan2012') & sel.outcome_name.isin(['Double support', 'Stride width', 'Stride length'])].sort_values(['outcome_name', 'load_pct_bm']).itertuples():
    row(f'{q.outcome_name}, shoulder bag {q.load_pct_bm}% BM', q)
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
