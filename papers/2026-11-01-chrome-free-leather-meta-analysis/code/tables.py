"""Step 5: tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os
import pandas as pd
from common import RES, EXT, ROOT

P = json.load(open(f'{RES}/prisma.json')); R = json.load(open(f'{RES}/meta.json'))
sc = pd.read_csv(f'{EXT}/study_characteristics.csv')
ex = pd.read_csv(f'{EXT}/extraction.csv'); rp = pd.read_csv(f'{EXT}/replicates.csv')
env = pd.read_csv(f'{EXT}/env_chem_evidence.csv')
f2 = lambda x: f'{x:.2f}'

t1 = ['**Table 1.** Study flow (PRISMA 2020-style counts). Searches run 21–22 October 2026.', '', '| Stage | Records or reports |', '|:--|--:|',
      f"| Records identified (OpenAlex {P['by_source']['OpenAlex']:,}; Europe PMC {P['by_source']['EuropePMC']:,}) | {P['records_identified']:,} |",
      f"| Unique records after removing duplicates | {P['unique_after_dedup']:,} |",
      f"| Removed by rule-based pre-screen (no leather, chrome, chrome-free and physical-outcome terms in title or abstract) | {P['excluded_prescreen']:,} |",
      f"| Titles and abstracts screened | {P['ta_screened']} |",
      f"| Excluded at title and abstract | {P['ta_excluded']} |",
      f"| Reports sought for full text | {P['reports_sought']} |",
      f"| Not retrieved: closed access | {P['not_retrieved_closed']} |",
      f"| Not retrieved: listed as open access but not obtained | {P['not_retrieved_oa']} |",
      f"| Retrieved from the database screen | {P['reports_retrieved']} |",
      f"| Added from another source (scoping brief; abstract lacked outcome terms) | {P['reports_other_sources']} |",
      f"| Duplicate reports of an included study | {P['reports_duplicate']} |",
      f"| Retrieved but not machine-readable | {P['reports_unreadable']} |",
      f"| Full texts assessed for eligibility | {P['reports_assessed']} |"]
for k, v in P['exclusion_reasons'].items(): t1.append(f'| Excluded: {k} | {v} |')
t1 += [f"| **Studies included** | **{P['studies_included']}** |"]
for o, l in [('tensile', 'tensile strength'), ('elongation', 'elongation at break'), ('tear', 'tear load'), ('ts', 'shrinkage temperature')]:
    t1.append(f"| With a usable mean ± SD contrast for {l} (with any contrast) | {P['studies_usable_for_pooling'][o]} ({P['studies_with_any_data'][o]}) |")

allr = pd.concat([ex[['study_id', 'arm_id', 'cf_class', 'outcome', 'n_stated', 'sd_cf', 'sd_cr']],
                  rp[rp.arm == 'cf'][['study_id', 'arm_id', 'cf_class', 'outcome']].drop_duplicates().assign(n_stated='yes', sd_cf=1, sd_cr=1)])
ab = {'tensile': 'TS', 'elongation': 'E', 'tear': 'T', 'ts': 'Ts'}
t2 = ['**Table 2.** Included studies. Classes are those of the chrome-free agents (a leather tested in several directions counts once). Outcomes: TS tensile strength, E elongation at break, T tear load, Ts shrinkage temperature; outcomes in brackets have no SD for both arms. Comparator: how the chrome-tanned comparison leather was obtained. Developer: the authors developed or optimised the chrome-free system tested.', '',
      '| Study | Substrate | Chrome-free arms (class) | Outcomes | Chrome comparator | n per arm stated | Developer |', '|:--|:--|:--|:--|:--|:--|:--|']
for _, s in sc.sort_values(['year', 'first_author']).iterrows():
    g = allr[allr.study_id == s.study_id]
    g = g.assign(agent=[a.split('_')[0] if s.study_id in ('bielak2022', 'cavali2022') else a for a in g.arm_id])  # directions of one leather count once
    cls = g.drop_duplicates('agent').cf_class.value_counts()
    outs = ', '.join((ab[o] if (g[g.outcome == o].sd_cf.notna() & g[g.outcome == o].sd_cr.notna()).any() else f'[{ab[o]}]') for o in ['tensile', 'elongation', 'tear', 'ts'] if o in set(g.outcome))
    nst = 'yes' if g.n_stated.eq('yes').all() else ('partly' if g.n_stated.isin(['yes', 'partial']).any() else 'no')
    name = f"{s.first_author} ({s.year})" + {0: '', 1: ' †', 2: ' ‡'}[int(s.integrity_flag)]
    t2.append(f"| {name} | {s.species} | " + '; '.join(f'{v} {k}' for k, v in cls.items()) + f" | {outs} | {s.comparator_source} | {nst} | {s.cf_developer} |")
t2.append(''); t2.append("‡ Same article published twice in the same issue of its journal; printed DOI not registered; retained in the primary analyses and reported without it (Table 3).")
t2.append("† Article whose text contains phrases typical of generated text (for example, \"user's anticipated benefits\" and \"the user's enzyme-activated system\") and a template page header; excluded from the primary analyses.")

M = R['models']; S = R['sensitivity']
def row(l, m): return f"| {l} | {m['k_studies']} ({m['k_effects']}) | {f2(m['est'])} | {f2(m['lo'])}–{f2(m['hi'])} | {f2(m['pi_lo'])}–{f2(m['pi_hi'])} |"
t3 = ['**Table 3.** Pooled ratios of means (chrome-free / chrome) from the two-level random-effects model (REML; 95% CI with t on studies − 1 degrees of freedom; prediction interval with t on studies − 2). Tensile strength met the pre-set threshold for pooling (about 15 studies) only with Gómez-García (2026); elongation and tear did not, and pooling them is a deviation from the protocol (§2.8). Ratios below 1 mean the chrome-free leather scored lower.', '',
      '| Analysis | Studies (contrasts) | Ratio | 95% CI | 95% prediction interval |', '|:--|--:|--:|--:|--:|',
      row('**Tensile strength, primary**', M['tensile']), row('Elongation at break (exploratory)', M['elongation']), row('Tear load (exploratory)', M['tear']),
      '| *Tensile strength, sensitivity analyses* | | | | |']
for k, l in [('n_missing_2', 'Missing n set to 2'), ('n_missing_5', 'Missing n set to 5'), ('impute_sd', 'Adding contrasts with imputed SDs (median CV)'),
             ('without_jia2022', 'Without the study reporting an SD of 0.00'), ('without_gomezgarcia2026', 'Without Gómez-García (2026; external chrome benchmark)'),
             ('without_aguilar2023', 'Without Aguilar (2023; duplicate publication, commercial chrome)'), ('without_both_outliers', 'Without both of these studies'),
             ('in_study_comparator_only', 'Chrome control tanned in-study only'),
             ('non_developer_only', 'Studies not by developers of the agent'), ('n_stated_only', 'Studies stating n for every arm')]:
    t3.append(row(l, S['tensile'][k]))
L = R['loo']['tensile']; 
t3.append(f"| Leave one study out (range of ratios) | {M['tensile']['k_studies'] - 1} each | {f2(L['min'])}–{f2(L['max'])} | | |")
t3.append('| *Tensile strength by chrome-free class (meta-regression, cell means)* | | | | |')
for c, v in R['moderators']['tensile']['cf_class'].items():
    t3.append(f"| {c.capitalize()} | {v['k_studies']} ({v['k_effects']}) | {f2(v['est'])} | {f2(v['lo'])}–{f2(v['hi'])} | |")
t3.append('| *Tensile strength, developer vs non-developer studies (ratio of ratios; exploratory)* | | | | |')
for k, l in [('developer', 'All studies'), ('developer_in_study_only', 'Chrome control tanned in-study only'), ('developer_without_both_outliers', 'Without Gómez-García and Aguilar')]:
    D = R['moderators']['tensile'][k]
    t3.append(f"| {l} | {D['k_dev_studies']} vs {D['k_nondev_studies']} | {f2(D['ratio_of_ratios'])} | {f2(D['lo'])}–{f2(D['hi'])} | |")

t4 = ['**Table 4.** Chemical, effluent, life-cycle and end-of-life evidence from studies that measured chrome and chrome-free leather or processes in the same study. Results are as reported by the authors; nothing was pooled. "Source read" states what the extraction rests on.', '',
      '| Domain | Study | Comparison | Method | Reported result | Source read |', '|:---|:--|:---|:---|:--------|:--|']
for _, e in env.iterrows():
    t4.append(f"| {e.domain} | {e.study} | {e.comparison} | {e.method} | {e.reported_result} | {e.source_read} |")

tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n\n' + '\n'.join(t4) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
