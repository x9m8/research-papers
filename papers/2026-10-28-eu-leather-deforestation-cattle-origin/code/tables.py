"""Regenerate the '## Tables' section of the manuscript from results/analysis.json."""
import json, re
from common import RES, ROOT, CF_SETS, ALL_RULES, CORE_RULE
o = json.load(open(f'{RES}/analysis.json'))
f = lambda v: f'{v:,.0f}'
M = [('Stage-wise tracing', 'Stage-wise tracing'), ('Pooled tracing (Laroche)', 'Pooled tracing'),
     ('Exporter: hides and leather', 'Direct imports, hides and leather'), ('Exporter: articles', 'Direct imports, articles'),
     ('Exporter: all direct imports', 'Direct imports, all')]
short = {'By-product (SWD), 2.5%': '2.5%', 'PEFCR, 3.5%': '3.5%', 'DeDuCE / SWD co-product, 5%': '5%', 'Mass (SWD), 8%': '8%', 'Mass (Laroche et al.), 10%': '10%',
         'Economic, price of the year': 'Econ.', 'Mass, FAOSTAT weights': 'FAO mass'}
s = o['mean_2015_2020']
t1 = ['**Table 1.** Deforestation embodied in EU27 leather, mean of 2015–2020 (hectares per year), by accounting method and allocation rule. Mean conversion factors of the Laroche et al. supplement (Kastner et al., 2024); exports above supply scaled down. Direct imports are attributed to the exporting country, as in the companion paper; EU use includes leather in EU-made cars and furniture. RHE, raw-hide equivalent; Econ., economic rule at prices of the year; FAO mass, mass share from FAOSTAT hide and carcass weights.', '',
      '| Method | RHE (kt) | ' + ' | '.join(short[r] for r in ALL_RULES) + ' |', '|------------------|' + '----:|' * (len(ALL_RULES) + 1)]
for m, lab in M: t1.append(f'| {lab} | {s[m]["rhe"] / 1e3:,.0f} | ' + ' | '.join(f(s[m][r]) for r in ALL_RULES) + ' |')
g = o['cf_grid_2015_2020']; gp = o['gap_2015_2020_kt']
t2 = ['**Table 2.** Sensitivity to conversion factors and to the treatment of exports that exceed supply, mean of 2015–2020, 5% allocation (hectares per year). The last three columns give the world total of such excess exports at each stage as a share of world exports at that stage, before correction. The three Laroche sets differ only in their factors for articles, so the direct-import figure for hides and leather is the same in all three.', '',
      '| Factor set | Direct imports, hides and leather | Stage-wise, exports scaled down | Stage-wise, supply topped up | Ratio, stage-wise to direct | Excess, tanned | Excess, finished | Excess, articles |', '|--------|-----:|-----:|-----:|-----:|----:|----:|----:|']
for cf in CF_SETS:
    a = g[f'{cf} | clip']; b = g[f'{cf} | topup']; x = a['Exporter: hides and leather']['ha']
    t2.append(f'| {cf} | {f(x)} | {f(a["Stage-wise tracing"]["ha"])} | {f(b["Stage-wise tracing"]["ha"])} | {a["Stage-wise tracing"]["ha"] / x:.2f}–{b["Stage-wise tracing"]["ha"] / x:.2f} | '
              + ' | '.join(f'{100 * gp[f"{cf} | stage {k}"]["share_of_world_exports"]:.1f}%' for k in (2, 3, 4)) + ' |')
bp = o['brazil_paraguay_2015_2020']; orig = ['Brazil', 'Paraguay', 'Bolivia (Plurinational State of)', 'India', 'China', 'Argentina', 'EU27']
t3 = ['**Table 3.** Cattle-origin countries in EU27 leather, mean of 2015–2020: raw-hide equivalent (thousand tonnes) and embodied deforestation at 5% (hectares per year), by accounting method.', '',
      '| Origin | Stage-wise, kt | Stage-wise, ha | Pooled, kt | Pooled, ha | Direct imports (hides and leather), kt | Direct imports (hides and leather), ha |', '|---|---:|---:|---:|---:|---:|---:|']
for c in orig:
    row = [bp[m][c] for m in ['Stage-wise tracing', 'Pooled tracing (Laroche)', 'Exporter: hides and leather']]
    t3.append(f'| {c.replace(" (Plurinational State of)", "")} | ' + ' | '.join(f'{r["rhe_kt"]:,.1f} | {f(r["ha"])}' for r in row) + ' |')
sc = o['scenarios_2015_2020']; base = sc['china=1.0, extra3=False, bovine=1.0']['ha']
rows = [('Core (supplement mean factors, exports scaled down, DeDuCE v2.1)', base),
        ("China's hide output halved in the tracing", sc['china=0.5, extra3=False, bovine=1.0']['ha']),
        ("China's hide output excluded from the tracing", sc['china=0.0, extra3=False, bovine=1.0']['ha']),
        ('Patent and composition leather (4114.20, 4115.10) added as finished leather', sc['china=1.0, extra3=True, bovine=1.0']['ha']),
        ('Three-quarters of article leather bovine', sc['china=1.0, extra3=False, bovine=0.75']['ha']),
        ('Supply topped up instead of exports scaled down', g['Laroche mean | topup']['Stage-wise tracing']['ha']),
        ('DeDuCE v2.0 instead of v2.1', s['Stage-wise tracing']['5% v2.0'])]
br = o['brazil_yield_sensitivity_2015_2020']
for y in (26, 30, 34):
    rows.append((f'Brazil hide output = head slaughtered × {y} kg (assumption)', br[f'Laroche mean | {y} kg']['stagewise_ha']))
t4 = ['**Table 4.** Sensitivity of the stage-wise estimate, mean of 2015–2020, 5% allocation. FAOSTAT implies a Brazilian hide yield of ' + f"{o['brazil_faostat_yield_kg_head']['min']:.0f}–{o['brazil_faostat_yield_kg_head']['max']:.0f}" + ' kg per head; the Brazil rows replace it with an assumed yield, which changes both the hides traced and Brazil\'s deforestation per tonne.', '', '| Scenario | Hectares per year | Change from core |', '|------------------|------:|------:|']
for lab, v in rows:
    chg = '—' if v == base else f'{100 * (v / base - 1):+.0f}%'.replace('-', '−')
    t4.append(f'| {lab} | {f(v)} | {chg} |')
txt = '\n'.join(t1 + [''] + t2 + [''] + t3 + [''] + t4) + '\n'
open(f'{RES}/tables.md', 'w').write(txt)
p = f'{ROOT}/manuscript/manuscript.md'
try:
    m = open(p).read()
    m = re.sub(r'## Tables\n.*?(?=\n## Figures)', '## Tables\n\n' + txt, m, flags=re.S)
    open(p, 'w').write(m)
except FileNotFoundError: pass
print(txt)
